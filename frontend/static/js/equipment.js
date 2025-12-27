let teams = [];
let equipmentList = [];

// Load teams and equipment on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadTeams();
    await loadEquipment();
});

async function loadTeams() {
    try {
        teams = await apiCall('/teams');
        const teamSelect = document.getElementById('equipmentTeamId');
        teamSelect.innerHTML = '<option value="">Select Team</option>';
        teams.forEach(team => {
            const option = document.createElement('option');
            option.value = team.id;
            option.textContent = team.name;
            teamSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading teams:', error);
    }
}

async function loadEquipment() {
    try {
        equipmentList = await apiCall('/equipment');
        renderEquipmentTable();
    } catch (error) {
        console.error('Error loading equipment:', error);
    }
}

function renderEquipmentTable() {
    const tbody = document.getElementById('equipmentTableBody');
    tbody.innerHTML = '';
    
    equipmentList.forEach(equipment => {
        const team = teams.find(t => t.id === equipment.maintenance_team_id);
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${equipment.name}</td>
            <td>${equipment.serial_number}</td>
            <td>${equipment.department}</td>
            <td>${equipment.location}</td>
            <td>${team ? team.name : 'N/A'}</td>
            <td><span class="badge bg-info">${equipment.maintenance_count || 0}</span></td>
            <td>
                ${equipment.is_scrapped 
                    ? '<span class="status-badge status-scrap">Scrapped</span>' 
                    : '<span class="status-badge status-repaired">Active</span>'}
            </td>
            <td>
                <button class="btn btn-sm btn-info" onclick="viewMaintenance(${equipment.id})" title="View Maintenance">
                    <i class="bi bi-tools"></i>
                </button>
                <button class="btn btn-sm btn-primary" onclick="editEquipment(${equipment.id})" title="Edit">
                    <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteEquipment(${equipment.id})" title="Delete">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function openEquipmentModal(equipmentId = null) {
    document.getElementById('equipmentForm').reset();
    document.getElementById('equipmentId').value = '';
    document.getElementById('equipmentModalTitle').textContent = equipmentId ? 'Edit Equipment' : 'Add Equipment';
    
    if (equipmentId) {
        const equipment = equipmentList.find(e => e.id === equipmentId);
        if (equipment) {
            document.getElementById('equipmentId').value = equipment.id;
            document.getElementById('equipmentName').value = equipment.name;
            document.getElementById('equipmentSerialNumber').value = equipment.serial_number;
            document.getElementById('equipmentDepartment').value = equipment.department;
            document.getElementById('equipmentLocation').value = equipment.location;
            document.getElementById('equipmentPurchaseDate').value = equipment.purchase_date;
            document.getElementById('equipmentWarrantyExpiry').value = equipment.warranty_expiry || '';
            document.getElementById('equipmentTeamId').value = equipment.maintenance_team_id;
            document.getElementById('equipmentIsScrapped').checked = equipment.is_scrapped;
        }
    }
}

async function saveEquipment() {
    const form = document.getElementById('equipmentForm');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const equipmentId = document.getElementById('equipmentId').value;
    const data = {
        name: document.getElementById('equipmentName').value,
        serial_number: document.getElementById('equipmentSerialNumber').value,
        department: document.getElementById('equipmentDepartment').value,
        location: document.getElementById('equipmentLocation').value,
        purchase_date: document.getElementById('equipmentPurchaseDate').value,
        warranty_expiry: document.getElementById('equipmentWarrantyExpiry').value || null,
        maintenance_team_id: parseInt(document.getElementById('equipmentTeamId').value),
        is_scrapped: document.getElementById('equipmentIsScrapped').checked
    };
    
    try {
        if (equipmentId) {
            await apiCall(`/equipment/${equipmentId}`, 'PUT', data);
            showNotification('Equipment updated successfully!', 'success');
        } else {
            await apiCall('/equipment', 'POST', data);
            showNotification('Equipment created successfully!', 'success');
        }
        
        bootstrap.Modal.getInstance(document.getElementById('equipmentModal')).hide();
        await loadEquipment();
    } catch (error) {
        showNotification('Error saving equipment: ' + error.message, 'danger');
    }
}

function editEquipment(id) {
    openEquipmentModal(id);
    const modal = new bootstrap.Modal(document.getElementById('equipmentModal'));
    modal.show();
}

async function deleteEquipment(id) {
    if (!confirm('Are you sure you want to delete this equipment?')) {
        return;
    }
    
    try {
        await apiCall(`/equipment/${id}`, 'DELETE');
        showNotification('Equipment deleted successfully!', 'success');
        await loadEquipment();
    } catch (error) {
        showNotification('Error deleting equipment: ' + error.message, 'danger');
    }
}

function viewMaintenance(equipmentId) {
    window.location.href = `/kanban?equipment=${equipmentId}`;
}

