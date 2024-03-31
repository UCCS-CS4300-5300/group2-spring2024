document.addEventListener('DOMContentLoaded', function() {
    // Get references to elements
    const prevWeekBtn = document.getElementById('prev-week-btn');
    const nextWeekBtn = document.getElementById('next-week-btn');
    const weekTitle = document.getElementById('week-title');
    const weekHeader = document.getElementById('week-header');
    const weekGrid = document.getElementById('week-grid');

    // Event listeners for previous and next week buttons
    prevWeekBtn.addEventListener('click', function() {
        updateWeek(-7); // Move back by 7 days (1 week)
    });

    nextWeekBtn.addEventListener('click', function() {
        updateWeek(7); // Move forward by 7 days (1 week)
    });

    // Function to update the week
    function updateWeek(days) {
        // Get the start date of the current week from the week title
        const currentWeekStart = new Date(weekTitle.textContent.split(' ')[2]);
        
        // Calculate the new start date of the week
        const newWeekStart = new Date(currentWeekStart);
        newWeekStart.setDate(newWeekStart.getDate() + days);
        
        // Calculate the new end date of the week (6 days later)
        const newWeekEnd = new Date(newWeekStart);
        newWeekEnd.setDate(newWeekEnd.getDate() + 6);
        
        // Update the week title with the new dates
        weekTitle.textContent = 'Week of ' + formatDate(newWeekStart) + ' - ' + formatDate(newWeekEnd);
        
        // Make AJAX request to retrieve tasks for the new week
        fetchTasks(newWeekStart, newWeekEnd);
    }

    // Function to format a date as 'YYYY-MM-DD'
    function formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return year + '-' + month + '-' + day;
    }

    // Function to fetch tasks for the given week
    function fetchTasks(startOfWeek, endOfWeek) {
        const url = '/get-tasks/?start_date=' + formatDate(startOfWeek) + '&end_date=' + formatDate(endOfWeek);
        
        fetch(url)
            .then(response => response.json())
            .then(tasks => {
                // Update the week view with new tasks data
                updateWeekView(tasks);
            })
            .catch(error => {
                console.error('Error fetching tasks:', error);
            });
    }

    // Function to update the week view with new tasks data
function updateWeekView(tasks) {
    // Clear existing tasks from week grid
    weekGrid.innerHTML = '';

    // Update week day headers in weekHeader (if necessary)

    // Add tasks for the week in weekGrid
    for (const day in tasks) {
        if (tasks.hasOwnProperty(day)) {
            const tasksForDay = tasks[day];
            const dayColumn = document.createElement('div');
            dayColumn.classList.add('col', 'weekday');

            // Create a header for the day
            const dayHeader = document.createElement('h3');
            dayHeader.textContent = day;
            dayColumn.appendChild(dayHeader);

            // Create a container for tasks of the day
            const tasksContainer = document.createElement('div');

            // Add each task to the tasks container
            tasksForDay.forEach(task => {
                const taskElement = document.createElement('div');
                taskElement.classList.add('task');
                taskElement.textContent = task.name; // Update to display task details as needed
                tasksContainer.appendChild(taskElement);
            });

            // Append tasks container to day column
            dayColumn.appendChild(tasksContainer);

            // Append day column to week grid
            weekGrid.appendChild(dayColumn);
        }
    }
}

});
