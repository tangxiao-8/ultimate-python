import asyncio
from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4


# Define a tuple with named records
@dataclass(order=True)
class TaskInfo:
    tid: str
    queued_at: datetime
    started_at: datetime


def current_time():
    """Return current time that is timezone-naive."""
    return datetime.now()


async def start_task(delay, task_id):
    """Start task_id after a certain delay in seconds."""
    queue_time = current_time()
    print(f"{queue_time} -> Queued task {task_id[:16]}...")
    await asyncio.sleep(delay)
    start_time = current_time()
    print(f"{start_time} -> Started task {task_id[:16]}...")
    return TaskInfo(tid=task_id, queued_at=queue_time, started_at=start_time)


async def start_batch():
    """Create a batch of tasks them concurrently."""
    print(f"{current_time()} -> Send initiation email")

    tasks = [asyncio.create_task(start_task(i * .01, f"{uuid4()}"))
             for i in range(1, 5)]

    # Gather all tasks for batch completion
    task_info_records = await asyncio.gather(*tasks)
    for result in task_info_records:
        assert result.queued_at < result.started_at

    print(f"{current_time()} -> Send completion email")


def main():
    asyncio.run(start_batch())


if __name__ == "__main__":
    main()
