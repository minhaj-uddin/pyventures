from tasks import check_spam

comment = "Congratulations! You have won a free prize!"

result = check_spam.apply_async((comment,))

print("Task result:", result.get())
