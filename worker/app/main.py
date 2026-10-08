import os
import time


def process_one_job() -> bool:
    """Claim one pending ack job and open its ticket.

    TODO:
      1. Select one jobs row where type = 'ack' and status = 'pending'.
      2. Set that ticket's status to 'open' and write acknowledgement.
      3. Set the job status to 'done'.
      4. Commit. Return True if a job was handled, False if the queue was empty.
    """
    raise NotImplementedError


def main():
    interval = int(os.environ.get("POLL_SECONDS", "5"))
    while True:
        try:
            process_one_job()
        except NotImplementedError:
            print("worker tick — implement process_one_job()")
        time.sleep(interval)


if __name__ == "__main__":
    main()
