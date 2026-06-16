# Edge Case: Mark Out of Valid Range

## What's the edge case?

The spec says `mark` is optional when creating a student, but it doesn't say anything about what happens if someone passes in a mark that doesn't make sense — like `-10`, `150`, or even `85.5`. These are technically valid JSON numbers, so without explicit validation, they'd get written straight into the database without any complaints.

## How I handled it

In both `POST /students` and `PUT /students/<id>`, I added a check before inserting or updating anything in the database:

```python
if not isinstance(mark, int) or mark < 0 or mark > 100:
    return jsonify({"error": "Mark must be an integer between 0 and 100"}), 404
```

So if the mark is a float, negative, or over 100, the request gets rejected with a 404 and a clear error message. Nothing gets written to the database.

## Why I handled it this way

Student marks should always be whole numbers between 0 and 100 — that's just how grading works. If we let garbage values in, the `/stats` endpoint would start returning a meaningless average or a max of 999, which defeats the whole purpose. Catching it early at the API layer keeps the database clean and makes debugging a lot easier down the line.
