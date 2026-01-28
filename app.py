from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import csv
import io
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "leetcode_tracker.db")

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'  # For flash messages

db = SQLAlchemy(app)

# ------------------ DATABASE MODEL ------------------
class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, nullable=False)  # Original day (can be reassigned)
    planned_day = db.Column(db.Integer, nullable=True)  # Assigned day for plans
    title = db.Column(db.String(200), nullable=False)
    leetcode_id = db.Column(db.Integer, nullable=False)
    topic = db.Column(db.String(100))
    difficulty = db.Column(db.String(20), default='Medium')  # Easy, Medium, Hard
    completed = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    completed_on = db.Column(db.DateTime)

# ------------------ INITIAL DATA ------------------
def seed_data():
    if Problem.query.first():
        return

    problems = [
        # Week 1 – Arrays & Strings
        (1, 1, 'Two Sum', 'Array', 'Easy'),
        (1, 217, 'Contains Duplicate', 'Array', 'Easy'),
        (1, 1920, 'Build Array from Permutation', 'Array', 'Easy'),
        (2, 26, 'Remove Duplicates from Sorted Array', 'Two Pointers', 'Easy'),
        (2, 125, 'Valid Palindrome', 'Two Pointers', 'Easy'),
        (2, 167, 'Two Sum II', 'Two Pointers', 'Medium'),
        (3, 121, 'Best Time to Buy and Sell Stock', 'Sliding Window', 'Easy'),
        (3, 643, 'Maximum Average Subarray I', 'Sliding Window', 'Easy'),
        (3, 1343, 'Number of Sub-arrays of Size K', 'Sliding Window', 'Medium'),
        (4, 3, 'Longest Substring Without Repeating Characters', 'Sliding Window', 'Medium'),
        (4, 424, 'Longest Repeating Character Replacement', 'Sliding Window', 'Medium'),
        (5, 303, 'Range Sum Query – Immutable', 'Prefix Sum', 'Easy'),
        (5, 560, 'Subarray Sum Equals K', 'Prefix Sum', 'Medium'),
        (5, 1480, 'Running Sum of 1D Array', 'Prefix Sum', 'Easy'),
        (6, 242, 'Valid Anagram', 'Hashing', 'Easy'),
        (6, 49, 'Group Anagrams', 'Hashing', 'Medium'),
        (6, 387, 'First Unique Character in a String', 'Hashing', 'Easy'),
        (7, 1, 'Two Sum', 'Revision', 'Easy'),  # Re-solve
        (7, 3, 'Longest Substring Without Repeating Characters', 'Revision', 'Medium'),
        (7, 560, 'Subarray Sum Equals K', 'Revision', 'Medium'),
        # Week 2 – Binary Search, Stack, Linked List
        (8, 704, 'Binary Search', 'Binary Search', 'Easy'),
        (8, 35, 'Search Insert Position', 'Binary Search', 'Easy'),
        (8, 278, 'First Bad Version', 'Binary Search', 'Easy'),
        (9, 34, 'Find First and Last Position', 'Binary Search', 'Medium'),
        (9, 33, 'Search in Rotated Sorted Array', 'Binary Search', 'Medium'),
        (10, 20, 'Valid Parentheses', 'Stack', 'Easy'),
        (10, 155, 'Min Stack', 'Stack', 'Medium'),
        (10, 232, 'Implement Queue using Stacks', 'Stack', 'Easy'),
        (11, 496, 'Next Greater Element I', 'Stack', 'Easy'),
        (11, 739, 'Daily Temperatures', 'Stack', 'Medium'),
        (12, 206, 'Reverse Linked List', 'Linked List', 'Easy'),
        (12, 21, 'Merge Two Sorted Lists', 'Linked List', 'Easy'),
        (13, 141, 'Linked List Cycle', 'Linked List', 'Easy'),
        (13, 19, 'Remove Nth Node From End', 'Linked List', 'Medium'),
        (14, 704, 'Binary Search', 'Revision', 'Easy'),  # Re-solve
        (14, 206, 'Reverse Linked List', 'Revision', 'Easy'),
        (14, 739, 'Daily Temperatures', 'Revision', 'Medium'),
        # Week 3 – Recursion, Trees, Backtracking
        (15, 509, 'Fibonacci Number', 'Recursion', 'Easy'),
        (15, 344, 'Reverse String', 'Recursion', 'Easy'),
        (15, 231, 'Power of Two', 'Recursion', 'Easy'),
        (16, 78, 'Subsets', 'Backtracking', 'Medium'),
        (16, 46, 'Permutations', 'Backtracking', 'Medium'),
        (17, 94, 'Inorder Traversal', 'Tree', 'Easy'),
        (17, 144, 'Preorder Traversal', 'Tree', 'Easy'),
        (17, 145, 'Postorder Traversal', 'Tree', 'Easy'),
        (18, 102, 'Level Order Traversal', 'Tree', 'Medium'),
        (18, 107, 'Level Order Traversal II', 'Tree', 'Medium'),
        (19, 104, 'Maximum Depth of Binary Tree', 'Tree', 'Easy'),
        (19, 110, 'Balanced Binary Tree', 'Tree', 'Easy'),
        (19, 543, 'Diameter of Binary Tree', 'Tree', 'Easy'),
        (20, 98, 'Validate BST', 'Tree', 'Medium'),
        (20, 235, 'Lowest Common Ancestor of BST', 'Tree', 'Medium'),
        (21, 78, 'Subsets', 'Revision', 'Medium'),  # Re-solve
        (21, 102, 'Level Order Traversal', 'Revision', 'Medium'),
        (21, 543, 'Diameter of Binary Tree', 'Revision', 'Easy'),
        # Week 4 – Graphs, DP & Greedy
        (22, 200, 'Number of Islands', 'Graph', 'Medium'),
        (22, 695, 'Max Area of Island', 'Graph', 'Medium'),
        (23, 994, 'Rotting Oranges', 'Graph', 'Medium'),
        (23, 733, 'Flood Fill', 'Graph', 'Easy'),
        (24, 70, 'Climbing Stairs', 'DP', 'Easy'),
        (24, 198, 'House Robber', 'DP', 'Medium'),
        (25, 300, 'Longest Increasing Subsequence', 'DP', 'Medium'),
        (25, 322, 'Coin Change', 'DP', 'Medium'),
        (26, 1143, 'Longest Common Subsequence', 'DP', 'Medium'),
        (26, 72, 'Edit Distance', 'DP', 'Hard'),  # Optional
        (27, 53, 'Maximum Subarray', 'Greedy', 'Medium'),
        (27, 455, 'Assign Cookies', 'Greedy', 'Easy'),
        (27, 122, 'Best Time to Buy and Sell Stock II', 'Greedy', 'Medium'),
        (28, 128, 'Longest Consecutive Sequence', 'Array', 'Medium'),
        (28, 215, 'Kth Largest Element in an Array', 'Array', 'Medium'),
        (29, 0, 'Mock Interview: Array Problem', 'Mock', 'Medium'),  # Placeholder
        (29, 0, 'Mock Interview: Tree Problem', 'Mock', 'Medium'),
        (29, 0, 'Mock Interview: DP Problem', 'Mock', 'Medium'),
        (30, 0, 'Final Revision: Sliding Window', 'Revision', 'Medium'),  # Placeholder
        (30, 0, 'Final Revision: Linked List', 'Revision', 'Easy'),
        (30, 0, 'Final Revision: Trees', 'Revision', 'Medium'),
        (30, 0, 'Final Revision: DP Patterns', 'Revision', 'Medium'),
    ]

    for day, lc_id, title, topic, diff in problems:
        db.session.add(Problem(day=day, planned_day=day, leetcode_id=lc_id, title=title, topic=topic, difficulty=diff))
    db.session.commit()

# ------------------ DATABASE INIT ------------------
with app.app_context():
    db.create_all()
    seed_data()




# ------------------ ROUTES ------------------
@app.route('/')
def dashboard():
    total = Problem.query.count()
    completed = Problem.query.filter_by(completed=True).count()
    pending = total - completed
    streak = calculate_streak()
    progress_percent = (completed / total * 100) if total > 0 else 0

    return render_template('dashboard.html', total=total, completed=completed, pending=pending, streak=streak, progress_percent=progress_percent)

@app.route('/problems')
def problems():
    query = Problem.query
    topic_filter = request.args.get('topic')
    status_filter = request.args.get('status')
    search = request.args.get('search')
    if topic_filter:
        query = query.filter_by(topic=topic_filter)
    if status_filter == 'completed':
        query = query.filter_by(completed=True)
    elif status_filter == 'pending':
        query = query.filter_by(completed=False)
    if search:
        query = query.filter(Problem.title.contains(search))
    from sqlalchemy import func
    data = query.order_by(func.coalesce(Problem.planned_day, Problem.day)).all()

    topics = db.session.query(Problem.topic).distinct().all()
    return render_template('problems.html', problems=data, topics=[t[0] for t in topics])
@app.route('/update/<int:problem_id>', methods=['POST'])
def update_status(problem_id):
    p = Problem.query.get(problem_id)
    if p:
        p.completed = not p.completed
        p.completed_on = datetime.now() if p.completed else None
        db.session.commit()
    return redirect(url_for('problems'))
@app.route('/toggle/<int:pid>', methods=['POST'])
def toggle(pid):
    p = Problem.query.get(pid)
    p.completed = not p.completed
    p.completed_on = datetime.now() if p.completed else None
    db.session.commit()
    return jsonify({'status': 'success', 'completed': p.completed})

@app.route('/notes/<int:pid>', methods=['POST'])
def notes(pid):
    p = Problem.query.get(pid)
    p.notes = request.form['notes']
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/daily-plans')
def daily_plans():
    plans = {}
    for day in range(1, 31):
        plans[day] = Problem.query.filter_by(planned_day=day).all()
    unassigned = Problem.query.filter_by(planned_day=None).all()
    return render_template('daily_plans.html', plans=plans, unassigned=unassigned)

@app.route('/assign/<int:pid>/<int:day>', methods=['POST'])
def assign(pid, day):
    p = Problem.query.get(pid)
    p.planned_day = day
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/calendar')
def calendar():
    days = []
    for day in range(1, 31):
        completed_count = Problem.query.filter_by(planned_day=day, completed=True).count()
        total_count = Problem.query.filter_by(planned_day=day).count()
        days.append({'day': day, 'completed': completed_count, 'total': total_count})
    return render_template('calendar.html', days=days)

@app.route('/stats')
def stats():
    topics = {}
    daily_progress = {day: 0 for day in range(1, 31)}
    for p in Problem.query.all():
        topics.setdefault(p.topic, {'done': 0, 'total': 0})
        topics[p.topic]['total'] += 1
        if p.completed:
            topics[p.topic]['done'] += 1
        if p.completed and p.completed_on:
            day = (p.completed_on - datetime(2023, 1, 1)).days + 1  # Adjust start date
            if 1 <= day <= 30:
                daily_progress[day] += 1
    return jsonify({'topics': topics, 'daily': list(daily_progress.values())})

@app.route('/export')
def export():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Day', 'Title', 'Topic', 'Difficulty', 'Completed', 'Notes'])
    for p in Problem.query.all():
        writer.writerow([p.planned_day or p.day, p.title, p.topic, p.difficulty, p.completed, p.notes])
    output.seek(0)
    return output.getvalue(), 200, {'Content-Type': 'text/csv', 'Content-Disposition': 'attachment; filename=progress.csv'}

def calculate_streak():
    streak = 0
    current_date = datetime.now().date()
    for i in range(30):
        day = current_date - timedelta(days=i)
        if Problem.query.filter(Problem.completed_on >= day, Problem.completed_on < day + timedelta(days=1)).first():
            streak += 1
        else:
            break
    return streak

# ------------------ MAIN ------------------
if __name__ == "__main__":
    app.run(debug=True)


