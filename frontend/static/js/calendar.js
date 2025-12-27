let currentDate = new Date();
let requests = [];
let equipmentList = [];

// Load data on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadEquipment();
    await loadRequests();
    renderCalendar();
});

async function loadEquipment() {
    try {
        equipmentList = await apiCall('/equipment');
    } catch (error) {
        console.error('Error loading equipment:', error);
    }
}

async function loadRequests() {
    try {
        requests = await apiCall('/maintenance-requests');
        renderCalendar();
    } catch (error) {
        console.error('Error loading requests:', error);
    }
}

function changeMonth(direction) {
    currentDate.setMonth(currentDate.getMonth() + direction);
    renderCalendar();
}

function renderCalendar() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    
    // Update month/year display
    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'];
    document.getElementById('calendarMonthYear').textContent = `${monthNames[month]} ${year}`;
    
    // Get first day of month and number of days
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDayOfWeek = firstDay.getDay();
    
    // Get preventive maintenance requests for this month
    const preventiveRequests = requests.filter(r => 
        r.request_type === 'Preventive' && r.scheduled_date
    );
    
    // Clear calendar
    const grid = document.getElementById('calendarGrid');
    grid.innerHTML = '';
    
    // Add day headers
    const dayHeaders = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    dayHeaders.forEach(day => {
        const header = document.createElement('div');
        header.className = 'calendar-day-header';
        header.textContent = day;
        grid.appendChild(header);
    });
    
    // Add empty cells for days before month starts
    for (let i = 0; i < startingDayOfWeek; i++) {
        const emptyDay = document.createElement('div');
        emptyDay.className = 'calendar-day other-month';
        grid.appendChild(emptyDay);
    }
    
    // Add days of the month
    const today = new Date();
    for (let day = 1; day <= daysInMonth; day++) {
        const dayElement = document.createElement('div');
        dayElement.className = 'calendar-day';
        
        const currentDayDate = new Date(year, month, day);
        const isToday = currentDayDate.toDateString() === today.toDateString();
        if (isToday) {
            dayElement.classList.add('today');
        }
        
        // Day number
        const dayNumber = document.createElement('div');
        dayNumber.style.fontWeight = 'bold';
        dayNumber.style.marginBottom = '5px';
        dayNumber.textContent = day;
        dayElement.appendChild(dayNumber);
        
        // Add events for this day
        const dayString = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        const dayEvents = preventiveRequests.filter(r => r.scheduled_date === dayString);
        
        dayEvents.forEach(event => {
            const eventElement = document.createElement('div');
            eventElement.className = 'event-item';
            
            if (event.is_overdue) {
                eventElement.classList.add('event-overdue');
            } else {
                eventElement.classList.add('event-preventive');
            }
            
            const equipment = equipmentList.find(e => e.id === event.equipment_id);
            eventElement.textContent = `${event.title} - ${equipment ? equipment.name : 'N/A'}`;
            eventElement.onclick = () => showEventDetails(event);
            dayElement.appendChild(eventElement);
        });
        
        grid.appendChild(dayElement);
    }
    
    // Add empty cells for days after month ends
    const totalCells = startingDayOfWeek + daysInMonth;
    const remainingCells = 42 - totalCells; // 6 weeks * 7 days
    for (let i = 0; i < remainingCells && totalCells + i < 42; i++) {
        const emptyDay = document.createElement('div');
        emptyDay.className = 'calendar-day other-month';
        grid.appendChild(emptyDay);
    }
}

function showEventDetails(event) {
    const equipment = equipmentList.find(e => e.id === event.equipment_id);
    const modalBody = document.getElementById('eventModalBody');
    
    modalBody.innerHTML = `
        <div class="mb-3">
            <strong>Title:</strong> ${event.title}
        </div>
        <div class="mb-3">
            <strong>Description:</strong> ${event.description || 'N/A'}
        </div>
        <div class="mb-3">
            <strong>Equipment:</strong> ${equipment ? equipment.name : 'N/A'}
        </div>
        <div class="mb-3">
            <strong>Type:</strong> ${event.request_type}
        </div>
        <div class="mb-3">
            <strong>Status:</strong> <span class="status-badge status-${event.status.toLowerCase().replace(' ', '-')}">${event.status}</span>
        </div>
        <div class="mb-3">
            <strong>Scheduled Date:</strong> ${formatDate(event.scheduled_date)}
        </div>
        ${event.duration ? `<div class="mb-3"><strong>Duration:</strong> ${event.duration} hours</div>` : ''}
        ${event.technician ? `<div class="mb-3"><strong>Technician:</strong> ${event.technician}</div>` : ''}
        ${event.is_overdue ? '<div class="alert alert-danger"><strong>This request is overdue!</strong></div>' : ''}
    `;
    
    const modal = new bootstrap.Modal(document.getElementById('eventModal'));
    modal.show();
}

