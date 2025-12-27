let requests = [];
let equipmentList = [];
let teams = [];

// Load data on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadEquipment();
    await loadTeams();
    await loadRequests();
    
    // Check for equipment filter in URL
    const urlParams = new URLSearchParams(window.location.search);
    const equipmentId = urlParams.get('equipment');
    if (equipmentId) {
        document.getElementById('requestEquipmentId').value = equipmentId;
        loadEquipmentTeam();
    }
});

async function loadEquipment() {
    try {
        equipmentList = await apiCall('/equipment');
        const select = document.getElementById('requestEquipmentId');
        select.innerHTML = '<option value="">Select Equipment</option>';
        equipmentList.forEach(eq => {
            const option = document.createElement('option');
            option.value = eq.id;
            option.textContent = `${eq.name} (${eq.serial_number})`;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading equipment:', error);
    }
}

async function loadTeams() {
    try {
        teams = await apiCall('/teams');
    } catch (error) {
        console.error('Error loading teams:', error);
    }
}

async function loadRequests() {
    try {
        requests = await apiCall('/maintenance-requests');
        renderKanban();
    } catch (error) {
        console.error('Error loading requests:', error);
    }
}

function renderKanban() {
    // Clear all columns
    document.getElementById('column-new').innerHTML = '';
    document.getElementById('column-in-progress').innerHTML = '';
    document.getElementById('column-repaired').innerHTML = '';
    document.getElementById('column-scrap').innerHTML = '';
    
    // Count requests per status
    const counts = {
        'New': 0,
        'In Progress': 0,
        'Repaired': 0,
        'Scrap': 0
    };
    
    requests.forEach(request => {
        counts[request.status]++;
        const card = createKanbanCard(request);
        const columnId = `column-${request.status.toLowerCase().replace(' ', '-')}`;
        document.getElementById(columnId).appendChild(card);
    });
    
    // Update counts
    document.getElementById('count-new').textContent = counts['New'];
    document.getElementById('count-in-progress').textContent = counts['In Progress'];
    document.getElementById('count-repaired').textContent = counts['Repaired'];
    document.getElementById('count-scrap').textContent = counts['Scrap'];
}

function createKanbanCard(request) {
    const card = document.createElement('div');
    card.className = `kanban-card status-${request.status.toLowerCase().replace(' ', '-')}`;
    if (request.is_overdue) {
        card.classList.add('overdue');
    }
    card.draggable = true;
    card.id = `request-${request.id}`;
    card.ondragstart = (e) => dragStart(e, request.id);
    
    const equipment = equipmentList.find(e => e.id === request.equipment_id);
    const team = teams.find(t => t.id === request.team_id);
    
    card.innerHTML = `
        <div class="d-flex justify-content-between align-items-start mb-2">
            <h6 class="mb-0">${request.title}</h6>
            ${request.is_overdue ? '<span class="badge bg-danger">Overdue</span>' : ''}
        </div>
        <p class="text-muted small mb-2">${equipment ? equipment.name : 'N/A'}</p>
        <p class="text-muted small mb-2">${request.description || 'No description'}</p>
        <div class="d-flex justify-content-between align-items-center">
            <small class="text-muted">${request.request_type}</small>
            <button class="btn btn-sm btn-outline-primary" onclick="editRequest(${request.id})">
                <i class="bi bi-pencil"></i>
            </button>
        </div>
        ${request.scheduled_date ? `<small class="text-muted d-block mt-2">Scheduled: ${formatDate(request.scheduled_date)}</small>` : ''}
    `;
    
    return card;
}

function dragStart(event, requestId) {
    event.dataTransfer.setData('text/plain', requestId.toString());
    event.currentTarget.classList.add('dragging');
}

function allowDrop(event) {
    event.preventDefault();
}

function drop(event) {
    event.preventDefault();
    const requestId = parseInt(event.dataTransfer.getData('text/plain'));
    const newStatus = event.currentTarget.getAttribute('data-status');
    
    // Remove dragging class from all cards
    document.querySelectorAll('.dragging').forEach(el => el.classList.remove('dragging'));
    
    updateRequestStatus(requestId, newStatus);
}

async function updateRequestStatus(requestId, newStatus) {
    try {
        await apiCall(`/maintenance-requests/${requestId}`, 'PUT', { status: newStatus });
        showNotification('Status updated successfully!', 'success');
        
        // If status is Scrap, also mark equipment as scrapped
        if (newStatus === 'Scrap') {
            const request = requests.find(r => r.id === requestId);
            if (request) {
                const equipment = equipmentList.find(e => e.id === request.equipment_id);
                if (equipment && !equipment.is_scrapped) {
                    await apiCall(`/equipment/${request.equipment_id}`, 'PUT', { is_scrapped: true });
                }
            }
        }
        
        await loadRequests();
    } catch (error) {
        showNotification('Error updating status: ' + error.message, 'danger');
    }
}

function loadEquipmentTeam() {
    const equipmentId = document.getElementById('requestEquipmentId').value;
    if (equipmentId) {
        const equipment = equipmentList.find(e => e.id === parseInt(equipmentId));
        if (equipment) {
            const team = teams.find(t => t.id === equipment.maintenance_team_id);
            document.getElementById('requestTeamId').value = equipment.maintenance_team_id;
            document.getElementById('requestTeamName').value = team ? team.name : 'N/A';
        }
    } else {
        document.getElementById('requestTeamId').value = '';
        document.getElementById('requestTeamName').value = '';
    }
}

function openRequestModal(requestId = null) {
    document.getElementById('requestForm').reset();
    document.getElementById('requestId').value = '';
    document.getElementById('requestModalTitle').textContent = requestId ? 'Edit Request' : 'Create Maintenance Request';
    document.getElementById('requestTeamName').value = '';
    document.getElementById('requestTeamId').value = '';
    
    if (requestId) {
        const request = requests.find(r => r.id === requestId);
        if (request) {
            document.getElementById('requestId').value = request.id;
            document.getElementById('requestTitle').value = request.title;
            document.getElementById('requestDescription').value = request.description || '';
            document.getElementById('requestEquipmentId').value = request.equipment_id;
            loadEquipmentTeam();
            document.getElementById('requestType').value = request.request_type;
            document.getElementById('requestTechnician').value = request.technician || '';
            document.getElementById('requestScheduledDate').value = request.scheduled_date || '';
            document.getElementById('requestDuration').value = request.duration || '';
        }
    }
}

async function saveRequest() {
    const form = document.getElementById('requestForm');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const requestId = document.getElementById('requestId').value;
    const data = {
        title: document.getElementById('requestTitle').value,
        description: document.getElementById('requestDescription').value,
        equipment_id: parseInt(document.getElementById('requestEquipmentId').value),
        technician: document.getElementById('requestTechnician').value || null,
        request_type: document.getElementById('requestType').value,
        scheduled_date: document.getElementById('requestScheduledDate').value || null,
        duration: document.getElementById('requestDuration').value ? parseInt(document.getElementById('requestDuration').value) : null
    };
    
    try {
        if (requestId) {
            await apiCall(`/maintenance-requests/${requestId}`, 'PUT', data);
            showNotification('Request updated successfully!', 'success');
        } else {
            await apiCall('/maintenance-requests', 'POST', data);
            showNotification('Request created successfully!', 'success');
        }
        
        bootstrap.Modal.getInstance(document.getElementById('requestModal')).hide();
        await loadRequests();
    } catch (error) {
        showNotification('Error saving request: ' + error.message, 'danger');
    }
}

function editRequest(id) {
    openRequestModal(id);
    const modal = new bootstrap.Modal(document.getElementById('requestModal'));
    modal.show();
}

