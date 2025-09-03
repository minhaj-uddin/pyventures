from tasks import sample_task

result = sample_task.delay(5)
print(result.get())
