
var myTitle = document.getElementById("title-app");

fetch("http://127.0.0.1:8000/", {
  method: "GET", // or 'PUT'
  headers: {
    "Content-Type": "application/json",
  },
})
  .then((response) => response.json())
  .then((data) => {
    myTitle.innerText = data.title
    const todos = data.todos;
    const ul = document.getElementById('myUL');
    todos.forEach(todo => {
      const li = document.createElement('li');
      li.appendChild(document.createTextNode(todo.name));
      if (todo.completed){
        li.className = "checked"
      }
      ul.appendChild(li);
    });
  })
  .catch((error) => {
    console.error("Error:", error);
  });


