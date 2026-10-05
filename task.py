from celery_app import celery_app
from datetime import datetime
import time

task_relationships = {}


# @celery_app.task
# def process_numbers():
#     total = 0

#     for number in range(1, 101):
#         total += number

#         processed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#         print(
#             f"Processing number: {number} | "
#             f"Current total: {total} | "
#             f"Time: {processed_at}"
#         )

#         time.sleep(1)

#     return total


# Start the Celery task with add_numbers
# parent class
@celery_app.task(bind=True)
def add_numbers(self):

    results = []
    child_task_ids = []
    parent_task_id = self.request.id

    """
    Process numbers from 1 to 100 and print the result of adding 1 to each
    """

    for number in range(1, 101):
        processed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"➕ [ADD] Number: {number} | " f"Result: {1 + number} | Time: {processed_at}")

        if number == 2:
            task = multiply_numbers.delay()
            child_task_ids.append(task.id)
            task_relationships[parent_task_id] = child_task_ids

            self.update_state(
                state="PROGRESS",
                meta={"child_task_ids": child_task_ids}
            )
            print(f"Started multiply_numbers task with ID: {task.id}")
        
        if number == 10:
            task = multiply_numbers.delay()
            child_task_ids.append(task.id)
            task_relationships[parent_task_id] = child_task_ids

            self.update_state(
                state="PROGRESS",
                meta={"child_task_ids": child_task_ids}
            )
            print(f"Started multiply_numbers task with ID: {task.id}")
        
        results.append({
            "number": number,
            "processed_at": processed_at                                                                                                                                                                                                                                                                                                                                                                                                                        
        })

        time.sleep(5)

    return {
    "results": results,
    "child_task_ids": child_task_ids
}






# Start the Celery task with multiply_numbers
#child class
@celery_app.task
def multiply_numbers():
    results = []

    """
    Process numbers from 1 to 100 and print the result of multiplying each by 1
    """

    for number in range(1, 101):
        processed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"✖️ [MULTIPLY] Number: {number} | " f"Result: {1 * number} | Time: {processed_at}")

        results.append({
            "number": number,
            "processed_at": processed_at
        })

        time.sleep(5)

    return results

# @celery_app.task
# def multiply_numbers_15():
#     results = []

#     for number in range(1, 101):
#         processed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#         print(
#             f"✖️ [MULTIPLY 15] Number: {number} | "
#             f"Result: {1 * number} | Time: {processed_at}"
#         )

#         results.append({
#             "number": number,
#             "processed_at": processed_at
#         })

#         time.sleep(3)

#     return results