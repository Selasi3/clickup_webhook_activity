from datetime import datetime, timedelta
from api.db import get_database
from api.services.clickup import ClickUpServices
from api.models.task_activity import TaskActivity, TaskHistory
from api.config import mongo_db_settings


clickup_service = ClickUpServices()

class TaskActivityService:
    def __init__(self):
        self.db_name = "task_activity"
        self.test_projects = ["Jesse AI", "Mediboard", "Levr"]
        self.valid_events = [
            "taskCreated",
            "taskUpdated",
            "taskCommentPosted",
            "taskAssigneeUpdated",
        ]

    async def create_task_activity(self, task_data):
        try:
            if task_data["event"] in self.valid_events:
                exist = await self.get_task_activity(task_data["task_id"])
                format = await self.format_data(task_data)
                # print({"exist": exist})

                db = await get_database()


                if exist:
                    # Update the 'current' field with data from 'format_data'
                    exist["current"].update(format["task"])
                    new_data = format["current"]

                    # Push the latest update to the 'activities' array
                    activity_update = TaskActivity(
                        update_by=format["email"],
                        date=datetime.now(),
                        update=new_data,
                        event=task_data["event"],
                    )

                    result = await db[self.db_name].update_one(
                        {"task_id": task_data["task_id"]},
                        {
                            "$set": {
                                "last_updated": new_data["date"],
                                "current": exist["current"],
                            },
                            "$push": {
                                "activities": activity_update.dict(),
                            },
                        },
                    )

                    return {"success": True}
                else:
                    formatted_data = await self.format_data(task_data)
                    new_data = formatted_data["current"]
                    task_data_format = formatted_data["task"]

                    task = TaskHistory(
                        task_id=task_data["task_id"],
                        last_updated=new_data["date"],
                        activities=[
                            TaskActivity(
                                update_by=formatted_data["email"],
                                date=datetime.now(),
                                update=new_data,
                                event=task_data["event"],
                            )
                        ],
                        current=task_data_format,
                    )
                    result = {}
                    if task_data_format["project"] in self.test_projects:
                        # print(task)
                        result = await db[self.db_name].insert_one(task.dict())
                    return {"success": True, "result": result}
            else:
                return {"success": False, "result": "Event not in scope"}

        except Exception as e:
            print(f"An error occurred while adding to history table: {str(e)}")
            return {"success": False, "error": str(e)}

    async def get_task_activity(self, task_id):
        db = await get_database()
        task_activity = await db[self.db_name].find_one({"task_id": task_id})
        return task_activity

    async def update_task_activity(self, task_id, task_activity):
        db = await get_database()
        await db[self.db_name].replace_one({"task_id": task_id}, task_activity)

    async def delete_task_activity(self, task_id):
        db = await get_database()
        await db[self.db_name].delete_one({"task_id": task_id})

    async def format_data(self, task_data):
        updates = {}
        task = {}
        if task_data["event"] in ["taskCreated", "taskUpdated"]:
            updates[task_data["history_items"][0]["field"]] = task_data[
                "history_items"
            ][0]["after"][task_data["history_items"][0]["field"]]
        elif task_data["event"] == "taskAssigneeUpdated":
            updates[task_data["history_items"][0]["field"]] = task_data[
                "history_items"
            ][0]["after"]["email"]
        else:
            updates[task_data["history_items"][0]["field"]] = task_data[
                "history_items"
            ][0]["comment"]["text_content"]

        date = int(task_data["history_items"][0]["date"])
        updates["date"] = datetime.utcfromtimestamp(date / 1000.0).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        task_raw_data = clickup_service.get_task(
            task_id=task_data["task_id"]
        )
        space = clickup_service.get_space(space_id=task_raw_data["space"]["id"])
        task_raw_data["space"] = {
            "id": space["id"],
            "name": space["name"],
        }
        task = self.filter_clickup_tasks(
            tasks=[task_raw_data], user_email="fake@gmail.com"
        )[0]

        return {
            "current": updates,
            "task": task,
            "email": task_data["history_items"][0]["user"]["email"],
        }

    def convert_time_miliseconds_to_hours(self, time_estimate):
        if time_estimate is None:
            return None

        # Convert milliseconds to hours
        time_estimate_hours = time_estimate / (1000 * 60 * 60)

        return f"{time_estimate_hours} hours"

    def convert_milliseconds_to_datetime(self, milliseconds):
        if milliseconds is None or milliseconds == "":
            return None

        # Convert milliseconds to seconds
        seconds = int(milliseconds) / 1000  # Ensure milliseconds is an integer

        # Convert seconds to a datetime object
        datetime_object = datetime.utcfromtimestamp(seconds)

        return datetime_object

    def remove_user_by_email(self, user_array, email_to_remove):
        # Use list comprehension to filter out the user with the specified email
        filtered_users = [
            user for user in user_array if user.get("email") != email_to_remove
        ]

        return filtered_users

    def filter_clickup_tasks(self, tasks, user_email):
        filtered_tasks = []

        for task in tasks:
            # Check if task["priority"] is not None before accessing ["priority"]["priority"]
            priority = (
                task["priority"]["priority"] if task["priority"] is not None else None
            )

            due_date = self.convert_milliseconds_to_datetime(task["due_date"])
            time_estimate = self.convert_time_miliseconds_to_hours(
                task["time_estimate"]
            )

            # Format due_date and time_estimate as strings
            due_date_str = due_date.strftime("%Y-%m-%d %H:%M:%S") if due_date else None

            # print({"unfiltered_tasks": task})

            filtered_task = {
                "name": task["name"],
                "due_date": due_date_str,
                "time_estimate": time_estimate,
                "priority": priority,
                "status": task["status"],
                "project": task["space"]["name"],
                "collaborators": self.remove_user_by_email(
                    user_array=task["assignees"], email_to_remove=user_email
                ),
                # "web_url": clickup_service.generate_task_web_url(task["id"]),
            }
            filtered_tasks.append(filtered_task)

        return filtered_tasks


    async def get_activities_by_project(self, project_name):
        try:
            db = await get_database()
            activities = []
            query = {
                "current.project": project_name
            }
            async for activity in db[self.db_name].find(query, {"_id": 0}):
                activities.append(activity)
            return activities

        except Exception as e:
            print(f"An error occurred while fetching project activities: {str(e)}")
            raise
