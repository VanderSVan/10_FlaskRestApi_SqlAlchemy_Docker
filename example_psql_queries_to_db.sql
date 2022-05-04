SELECT student_id, group_id, CONCAT(first_name, ' ', last_name) AS full_name, COUNT(course_id) AS number_of_courses
FROM students
LEFT JOIN students_courses USING(student_id)
GROUP BY student_id
ORDER BY student_id;

SELECT course_id, COUNT(student_id) AS number_of_students
FROM students
LEFT JOIN students_courses USING(student_id)
GROUP BY course_id
ORDER BY course_id;

SELECT COUNT(student_id) 
FROM students
WHERE student_id = ANY(SELECT student_id FROM students
				 	   LEFT JOIN students_courses USING(student_id)
					   GROUP BY student_id
				       HAVING COUNT(course_id) = 3)


