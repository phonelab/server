function participant() {

	if( document.getElementById('id_user_type').value == 'P' ) {
		if(document.getElementById('id_groupname')!=null) {
		var table = document.getElementById('reg_table');
		table.deleteRow(-1);
	}
	}
	else {
		if(document.getElementById('id_groupname')==null) {
			var table = document.getElementById('reg_table');

			var rowCount = table.rows.length;
            var row = table.insertRow(rowCount);
 
            var cell1 = row.insertCell(0);
            var element1 = document.createElement("label");
            element1.innerHTML = 'Group Name'
            cell1.appendChild(element1);
 
            var cell2 = row.insertCell(1);
            var element2 = document.createElement("input");
            element2.type = "text";
            element2.name = 'groupname'
            element2.id = 'id_groupname'
            cell2.appendChild(element2);
		}
	}
}