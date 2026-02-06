fetch("http://localhost:5000/users", {
    method:"GET"
}).then(response => {
    if (!response.ok){
        throw new Error("Error http: ", + response.status);
    }
    return response.json();
})
.then(data => {
    const tbody = document.getElementById("datatable");
    tbody.innerHTML = "";

    data.data.forEach((user) => {
        tbody.innerHTML += `
         <tr>
            <td>${user.id}</td>
            <td>${user.name}</td>
            <td>${user.lastname}</td>
            <td>${user.phone}</td>
            <td>${user.dob}</td>
            <td>${user.username}</td>
            <td>${user.status === true ? "Active" : "Inactive"}</td>
         </tr>
        `;

    })
})
.catch(error => {
    document.getElementById("datatable").innerHTML = `
    <tr>
        <td colspan = "7">error loading data.... ${error}</td> 
    </tr>
    `;
    console.log(error);

})