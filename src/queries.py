QUERIES = {
    "rooms_with_students_count": """
        SELECT r.name, COUNT(s.id) as students_count
        FROM rooms r
        LEFT JOIN students s ON r.id = s.room_id
        GROUP BY r.id;
    """,
    "top_5_smallest_average_age": """
        SELECT r.name,  AVG(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) as average_age
        FROM rooms r
        LEFT JOIN students s ON r.id = s.room_id
        GROUP BY r.id
        ORDER BY average_age ASC
        LIMIT 5;
    """,
    "top_5_largest_age_diff": """
        SELECT r.name,  MAX(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) - MIN(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) as age_diff
        FROM rooms r
        LEFT JOIN students s ON r.id = s.room_id
        GROUP BY r.id
        ORDER BY age_diff DESC
        LIMIT 5;
    """,
    "rooms_with_mixed_sex": """
        SELECT r.name
        FROM rooms r
        JOIN students s ON r.id = s.room_id
        GROUP BY r.id
        HAVING COUNT(DISTINCT s.sex) > 1;
    """
}
