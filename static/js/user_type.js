window.onload = typecheck;

function typecheck() {
	var x=document.getElementById("id_user_type");
	x.onchange = function() {
			
		if(this.value=="member") {
			if(!document.getElementById("id_leadername")) {
				var element = document.createElement("input");

				element.setAttribute("type", "text");
				var table = document.getElementById("reg_table")
				var rowCount = table.rows.length;
            	var row = table.insertRow(rowCount);

            	var cell1 = row.insertCell(0);
            	var label = document.createElement("label");
            	label.setAttribute("for", "id_leadername");
            	label.innerHTML= "Your Leader's username:";
            	cell1.appendChild(label);

            	var cell2 = row.insertCell(1);
            	var textbox = document.createElement("input");
            	textbox.setAttribute("type", "text");
            	textbox.setAttribute("id", "id_leadername");
            	textbox.setAttribute("name", "leader_name");
            	textbox.setAttribute("maxlength", "30");
            	cell2.appendChild(textbox);
        	}
		}

		else {
			if(document.getElementById("id_leadername")) {
				var table = document.getElementById("reg_table");
				var row_count = table.rows.length;
				table.deleteRow(row_count-1);
			}
		}	

	}
}

