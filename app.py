import streamlit as st
from database import init_db, register_student, get_student, add_event, get_events, get_completed_events, enroll_student, get_participation, mark_event_completed, get_participation_count, announce_result, get_participants, delete_event
from security import hash_password, verify_mobile
import time
from datetime import datetime

# Initialize database
init_db()

# Session state for user management
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'last_add_time' not in st.session_state:
    st.session_state.last_add_time = 0
if 'show_participants' not in st.session_state:
    st.session_state.show_participants = {}
if 'active_section' not in st.session_state:
    st.session_state.active_section = "Add Event"  # Default section for admin

# Custom CSS with animations and no white space/lines
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #e0f7fa, #f0f4f8);
        font-family: 'Arial', sans-serif;
        animation: fadeIn 1s ease-in;
    }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    .header {
        background: linear-gradient(90deg, #2c3e50, #3498db);
        color: white;
        text-align: center;
        padding: 20px;
        font-size: 36px;
        font-weight: bold;
        border-bottom: 4px solid #2980b9;
        margin-bottom: 5px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        animation: slideDown 0.5s ease-out;
    }
    @keyframes slideDown { from { transform: translateY(-50px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #34495e, #2c3e50);
        color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    .stButton>button {
        background: linear-gradient(90deg, #3498db, #2980b9);
        color: white;
        border-radius: 25px;
        padding: 10px 25px;
        margin: 5px 0;
        font-size: 16px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #2980b9, #1e6b8c);
        transform: scale(1.05);
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    }
    .stTextInput > div > input, .stSelectbox > div > select, .stDateInput > div > input, .stTimeInput > div > input {
        border-radius: 15px;
        border: 2px solid #3498db;
        padding: 10px;
        background: rgba(255, 255, 255, 0.9);
        transition: all 0.3s ease;
    }
    .stTextInput > div > input:focus, .stSelectbox > div > select:focus, .stDateInput > div > input:focus, .stTimeInput > div > input:focus {
        border-color: #2980b9;
        box-shadow: 0 0 10px rgba(52, 152, 219, 0.5);
    }
    .main-content {
        padding: 10px;
        animation: slideIn 0.5s ease-out;
    }
    @keyframes slideIn { from { transform: translateX(-50px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
    .event-container {
        max-height: 70vh;
        overflow-y: auto;
        padding: 0;
        background: none;
        border: none;
        box-shadow: none;
        margin: 0;
    }
    .event-card {
        background: linear-gradient(135deg, #e0f7fa, #f0f4f8); /* Matches background to avoid white lines */
        padding: 8px;
        margin: 0;
        border: none;
        box-shadow: none;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: popIn 0.5s ease-out;
    }
    @keyframes popIn { from { transform: scale(0.9); opacity: 0; } to { transform: scale(1); opacity: 1; } }
    .event-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    .participant-list {
        max-height: 250px;
        overflow-y: auto;
        border: none;
        padding: 5px;
        background: none;
        margin: 0;
        display: none;
        animation: fadeInUp 0.3s ease-out;
    }
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
    .participant-list.visible {
        display: block;
    }
    .invalid-event {
        background-color: #ffebee;
        padding: 5px;
        margin: 0;
        color: #c62828;
        animation: shake 0.5s ease-out;
    }
    @keyframes shake {
        0% { transform: translateX(0); }
        25% { transform: translateX(-4px); }
        50% { transform: translateX(4px); }
        75% { transform: translateX(-4px); }
        100% { transform: translateX(0); }
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 5px;
        margin: 0;
        text-align: center;
        animation: bounceIn 0.5s ease-out;
    }
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 5px;
        margin: 0;
        text-align: center;
        animation: bounceIn 0.5s ease-out;
    }
    @keyframes bounceIn { from { transform: scale(0.8); opacity: 0; } to { transform: scale(1); opacity: 1; } }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown('<div class="header">TechConnect</div>', unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("Navigation")
if st.session_state.logged_in:
    if st.session_state.user_role == "student":
        if st.sidebar.button("Profile"):
            st.session_state.active_section = "Profile"
            st.rerun()
        if st.sidebar.button("Live Events"):
            st.session_state.active_section = "Live Events"
            st.rerun()
        if st.sidebar.button("Completed Events"):
            st.session_state.active_section = "Completed Events"
            st.rerun()
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.session_state.user_data = None
            st.session_state.active_section = None
            st.rerun()
    elif st.session_state.user_role == "admin":
        if st.sidebar.button("Add Event"):
            st.session_state.active_section = "Add Event"
            st.rerun()
        if st.sidebar.button("Manage Events"):
            st.session_state.active_section = "Manage Events"
            st.rerun()
        if st.sidebar.button("View Completed Events"):
            st.session_state.active_section = "View Completed Events"
            st.rerun()
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.session_state.user_data = None
            st.session_state.active_section = None
            st.rerun()
else:
    choice = st.sidebar.radio("Choose Role", ["Student", "Admin"])

# Main content with single dynamic section
st.markdown('<div class="main-content">', unsafe_allow_html=True)
if not st.session_state.logged_in:
    if choice == "Student":
        st.subheader("Student Login/Register")
        mode = st.radio("Select Mode", ["Login", "Register"], horizontal=True, key="mode_radio")
        
        if mode == "Register":
            with st.form(key="register_form"):
                roll_no = st.text_input("Roll No", key="reg_roll_no")
                name = st.text_input("Name", key="reg_name")
                mobile = st.text_input("Mobile", key="reg_mobile")
                email = st.text_input("Email", key="reg_email")
                branch = st.selectbox("Branch", ["CSE", "CSM", "CAD", "IOT", "ECE", "MECH", "EEE"], key="reg_branch")
                year = st.selectbox("Year", ["1st", "2nd", "3rd"], key="reg_year")
                password = st.text_input("Password", type="password", key="reg_password")
                submit = st.form_submit_button("Register")
                
                if submit:
                    if not verify_mobile(mobile):
                        st.markdown('<div class="error-message">Invalid mobile number! Must be 10 digits.</div>', unsafe_allow_html=True)
                    elif not all([roll_no, name, mobile, email, branch, year, password]):
                        st.markdown('<div class="error-message">All fields are required!</div>', unsafe_allow_html=True)
                    else:
                        try:
                            register_student(roll_no, name, mobile, email, branch, year, hash_password(password))
                            st.markdown('<div class="success-message">Registered successfully! Logging you in...</div>', unsafe_allow_html=True)
                            time.sleep(1)
                            student = get_student(roll_no)
                            if student and student[6] == hash_password(password):
                                st.session_state.logged_in = True
                                st.session_state.user_role = "student"
                                st.session_state.user_data = student
                                st.session_state.active_section = "Profile"
                                st.rerun()
                            else:
                                st.markdown('<div class="error-message">Login failed after registration.</div>', unsafe_allow_html=True)
                        except ValueError as e:
                            st.markdown(f'<div class="error-message">{str(e)}</div>', unsafe_allow_html=True)
        else:
            with st.form(key="login_form"):
                roll_no = st.text_input("Roll No", key="login_roll_no")
                password = st.text_input("Password", type="password", key="login_password")
                submit = st.form_submit_button("Login")
                
                if submit:
                    if not roll_no or not password:
                        st.markdown('<div class="error-message">Roll No and Password are required!</div>', unsafe_allow_html=True)
                    else:
                        student = get_student(roll_no)
                        if student and student[6] == hash_password(password):
                            st.session_state.logged_in = True
                            st.session_state.user_role = "student"
                            st.session_state.user_data = student
                            st.session_state.active_section = "Profile"
                            st.rerun()
                        else:
                            st.markdown('<div class="error-message">Invalid roll no or password.</div>', unsafe_allow_html=True)
    elif choice == "Admin":
        st.subheader("Admin Login")
        admin_password = st.text_input("Admin Password", type="password", key="admin_password")
        if st.button("Login", key="admin_login"):
            if admin_password == "admin123":
                st.session_state.logged_in = True
                st.session_state.user_role = "admin"
                st.session_state.active_section = "Add Event"
                st.rerun()
            else:
                st.markdown('<div class="error-message">Invalid admin password. Please use \'admin123\'.</div>', unsafe_allow_html=True)
else:
    if st.session_state.user_role == "student":
        st.subheader(f"Welcome, {st.session_state.user_data[1]}!")
        if st.session_state.active_section == "Profile":
            st.write("**Profile Details**")
            st.write(f"Roll No: {st.session_state.user_data[0]}")
            st.write(f"Name: {st.session_state.user_data[1]}")
            st.write(f"Mobile: {st.session_state.user_data[2]}")
            st.write(f"Email: {st.session_state.user_data[3]}")
            st.write(f"Branch: {st.session_state.user_data[4]}")
            st.write(f"Year: {st.session_state.user_data[5]}")
        elif st.session_state.active_section == "Live Events":
            st.write("**Live Events**")
            live_events = get_events()
            if live_events:
                with st.container():
                    st.write('<div class="event-container">', unsafe_allow_html=True)
                    for event in live_events:
                        try:
                            start_date = datetime.strptime(event[3], "%Y-%m-%d %H:%M:%S")
                            due_date = datetime.strptime(event[2], "%Y-%m-%d")
                            formatted_start = start_date.strftime("%B %d, %Y %H:%M")
                            formatted_due = due_date.strftime("%B %d, %Y")
                        except ValueError:
                            st.markdown(f'<div class="invalid-event">Invalid date format for event {event[1]}.</div>', unsafe_allow_html=True)
                            continue
                        with st.expander(f"**{event[1]}** - Event Starts: {formatted_start}, Enrollment Deadline: {formatted_due}", expanded=False):
                            participation = get_participation(st.session_state.user_data[0], event[0])
                            if participation and participation[2] == 1:
                                st.write("Status: Enrolled")
                            else:
                                if st.button("Enroll", key=f"enroll_{event[0]}"):
                                    enroll_student(st.session_state.user_data[0], event[0])
                                    st.markdown('<div class="success-message">Enrolled successfully!</div>', unsafe_allow_html=True)
                                    time.sleep(1)
                                    st.rerun()
                    st.write('</div>', unsafe_allow_html=True)
            else:
                st.write("No live events available.")
        elif st.session_state.active_section == "Completed Events":
            st.write("**Completed Events**")
            completed_events = get_completed_events()
            if completed_events:
                with st.container():
                    st.write('<div class="event-container">', unsafe_allow_html=True)
                    for event in completed_events:
                        try:
                            start_date = datetime.strptime(event[3], "%Y-%m-%d %H:%M:%S")
                            due_date = datetime.strptime(event[2], "%Y-%m-%d")
                            formatted_start = start_date.strftime("%B %d, %Y %H:%M")
                            formatted_due = due_date.strftime("%B %d, %Y")
                        except ValueError:
                            st.markdown(f'<div class="invalid-event">Invalid date format for event {event[1]}.</div>', unsafe_allow_html=True)
                            continue
                        with st.expander(f"**{event[1]}** - Event Started: {formatted_start}, Enrollment Ended: {formatted_due}", expanded=False):
                            winners = [p for p in get_participants(event[0]) if p[5]]
                            if winners:
                                st.write("**Winners:**")
                                for i, (roll_no, name, _, _, _, result) in enumerate(sorted(winners, key=lambda x: ['1st', '2nd'].index(x[5]) if x[5] in ['1st', '2nd'] else 2), 1):
                                    st.write(f"{name} (Roll No: {roll_no}) - {result}")
                                    if st.session_state.user_data and st.session_state.user_data[0] == roll_no:
                                        st.markdown(f'<div class="success-message">Congratulations! You won the {event[1]} and got {result} rank!</div>', unsafe_allow_html=True)
                            else:
                                st.write("No winners announced yet.")
                    st.write('</div>', unsafe_allow_html=True)
            else:
                st.write("No completed events available.")
    elif st.session_state.user_role == "admin":
        st.subheader("Admin Dashboard")
        if st.session_state.active_section == "Add Event":
            st.write("**Add New Event**")
            with st.form(key="add_event_form"):
                name = st.text_input("Name", key="add_name")
                enrollment_deadline = st.date_input("Enrollment Deadline", value=datetime(2025, 4, 14), key="add_deadline")
                event_start_date = st.date_input("Event Start Date", value=datetime(2025, 4, 15), key="add_start_date")
                event_start_time = st.time_input("Event Start Time", value=datetime(2025, 4, 15, 10, 0).time(), key="add_start_time")
                instructions = st.text_area("Instructions", key="add_instructions")
                submit = st.form_submit_button("Add Event")
                current_time = time.time()
                if submit and name and enrollment_deadline and event_start_date and event_start_time:
                    if current_time - st.session_state.last_add_time > 2:  # Debounce: 2-second delay
                        due_date_str = enrollment_deadline.strftime("%Y-%m-%d")
                        start_time_str = f"{event_start_date.strftime('%Y-%m-%d')} {event_start_time.strftime('%H:%M:%S')}"
                        add_event(name, due_date_str, start_time_str, instructions)
                        st.markdown('<div class="success-message">Event added successfully!</div>', unsafe_allow_html=True)
                        st.session_state.last_add_time = current_time
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.markdown('<div class="error-message">Please wait 2 seconds before adding another event.</div>', unsafe_allow_html=True)
        elif st.session_state.active_section == "Manage Events":
            st.write("**Manage Events**")
            live_events = get_events()  # Only live events (is_completed = 0)
            if live_events:
                with st.container():
                    st.write('<div class="event-container">', unsafe_allow_html=True)
                    for event in live_events:
                        try:
                            start_date = datetime.strptime(event[3], "%Y-%m-%d %H:%M:%S")
                            due_date = datetime.strptime(event[2], "%Y-%m-%d")
                            formatted_start = start_date.strftime("%B %d, %Y %H:%M")
                            formatted_due = due_date.strftime("%B %d, %Y")
                        except ValueError:
                            st.markdown(f'<div class="invalid-event">Invalid date format for event {event[1]}.</div>', unsafe_allow_html=True)
                            continue
                        with st.expander(f"**{event[1]}** - Starts: {formatted_start}, Deadline: {formatted_due}", expanded=False):
                            st.write(f"Instructions: {event[4]}")
                            if st.button("View Participants", key=f"view_participants_{event[0]}"):
                                st.session_state.show_participants[event[0]] = not st.session_state.show_participants.get(event[0], False)
                            if st.session_state.show_participants.get(event[0], False):
                                participants = get_participants(event[0])
                                sort_by = st.selectbox("Sort by", ["Name", "Branch", "Year", "Enrollment Time"], key=f"sort_{event[0]}")
                                if sort_by == "Name":
                                    participants.sort(key=lambda x: x[1])
                                elif sort_by == "Branch":
                                    participants.sort(key=lambda x: x[2])
                                elif sort_by == "Year":
                                    participants.sort(key=lambda x: x[3])
                                elif sort_by == "Enrollment Time":
                                    participants.sort(key=lambda x: x[4])
                                with st.container():
                                    st.write('<div class="participant-list visible">', unsafe_allow_html=True)
                                    for p in participants:
                                        st.write(f"- {p[1]} (Roll No: {p[0]}, Branch: {p[2]}, Year: {p[3]}, Enrolled: {p[4]})")
                                    st.write('</div>', unsafe_allow_html=True)
                            participant_options = {p[0]: f"{p[1]} (Roll No: {p[0]})" for p in get_participants(event[0])}
                            selected_participants = st.multiselect("Select winners", options=list(participant_options.values()), key=f"select_{event[0]}")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                if st.button("Mark Completed", key=f"complete_{event[0]}"):
                                    mark_event_completed(event[0])
                                    st.markdown('<div class="success-message">Event marked as completed!</div>', unsafe_allow_html=True)
                                    time.sleep(1)
                                    st.rerun()
                            with col2:
                                if st.button("Announce Winners", key=f"announce_{event[0]}"):
                                    if selected_participants and get_participation_count(event[0]) > 0:
                                        for i, participant_name in enumerate(selected_participants[:2], 1):
                                            roll_no = next(k for k, v in participant_options.items() if v == participant_name)
                                            rank = "1st" if i == 1 else "2nd"
                                            announce_result(roll_no, event[0], rank)
                                        st.markdown('<div class="success-message">Winners announced!</div>', unsafe_allow_html=True)
                                        time.sleep(1)
                                        st.rerun()
                                    else:
                                        st.markdown('<div class="error-message">No participants selected.</div>', unsafe_allow_html=True)
                            with col3:
                                if st.button("Delete Event", key=f"delete_{event[0]}"):
                                    delete_event(event[0])
                                    st.markdown('<div class="success-message">Event deleted!</div>', unsafe_allow_html=True)
                                    time.sleep(1)
                                    st.rerun()
                    st.write('</div>', unsafe_allow_html=True)
            else:
                st.write("No live events to manage.")
        elif st.session_state.active_section == "View Completed Events":
            st.write("**Completed Events**")
            completed_events = get_completed_events()  # Only completed events (is_completed = 1)
            if completed_events:
                with st.container():
                    st.write('<div class="event-container">', unsafe_allow_html=True)
                    for event in completed_events:
                        try:
                            start_date = datetime.strptime(event[3], "%Y-%m-%d %H:%M:%S")
                            due_date = datetime.strptime(event[2], "%Y-%m-%d")
                            formatted_start = start_date.strftime("%B %d, %Y %H:%M")
                            formatted_due = due_date.strftime("%B %d, %Y")
                        except ValueError:
                            st.markdown(f'<div class="invalid-event">Invalid date format for event {event[1]}.</div>', unsafe_allow_html=True)
                            continue
                        with st.expander(f"**{event[1]}** - Started: {formatted_start}, Ended: {formatted_due}", expanded=False):
                            if st.button("View Participants", key=f"view_participants_completed_{event[0]}"):
                                st.session_state.show_participants[event[0]] = not st.session_state.show_participants.get(event[0], False)
                            if st.session_state.show_participants.get(event[0], False):
                                participants = get_participants(event[0])
                                sort_by = st.selectbox("Sort by", ["Name", "Branch", "Year", "Enrollment Time"], key=f"sort_completed_{event[0]}")
                                if sort_by == "Name":
                                    participants.sort(key=lambda x: x[1])
                                elif sort_by == "Branch":
                                    participants.sort(key=lambda x: x[2])
                                elif sort_by == "Year":
                                    participants.sort(key=lambda x: x[3])
                                elif sort_by == "Enrollment Time":
                                    participants.sort(key=lambda x: x[4])
                                with st.container():
                                    st.write('<div class="participant-list visible">', unsafe_allow_html=True)
                                    for p in participants:
                                        st.write(f"- {p[1]} (Roll No: {p[0]}, Branch: {p[2]}, Year: {p[3]}, Enrolled: {p[4]})")
                                    st.write('</div>', unsafe_allow_html=True)
                            winners = [p for p in get_participants(event[0]) if p[5]]
                            if winners:
                                st.write("**Winners:**")
                                for p in sorted(winners, key=lambda x: ['1st', '2nd'].index(x[5]) if x[5] in ['1st', '2nd'] else 2):
                                    st.write(f"- {p[1]} (Roll No: {p[0]}) - {p[5]}")
                            if st.button("Delete Event", key=f"delete_completed_{event[0]}"):
                                delete_event(event[0])
                                st.markdown('<div class="success-message">Event deleted!</div>', unsafe_allow_html=True)
                                time.sleep(1)
                                st.rerun()
                    st.write('</div>', unsafe_allow_html=True)
            else:
                st.write("No completed events to view.")
st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    pass