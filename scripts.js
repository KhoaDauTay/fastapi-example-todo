// Create a "close" button and append it to each list item
var myNodelist = document.getElementsByTagName("LI");

var i;
for (i = 0; i < myNodelist.length; i++) {
    var span = document.createElement("SPAN");
    var txt = document.createTextNode("\u00D7");
    span.className = "close";
    span.appendChild(txt);
    myNodelist[i].appendChild(span);
}

// Click on a close button to hide the current list item
var close = document.getElementsByClassName("close");
var i;
for (i = 0; i < close.length; i++) {
  close[i].onclick = function() {
    var div = this.parentElement;
    div.style.display = "none";
  }
}

// Add a "checked" symbol when clicking on a list item
var list = document.querySelector('ul');
list.addEventListener('click', function (ev) {
    if (ev.target.tagName === 'LI') {
        var completed = true;
        if (ev.target.className === "checked"){
            completed = false;
        }
        var name = ev.target.textContent
        fetch(`http://127.0.0.1:8000/todos/${name}`, {
            method: "PUT", // or 'PUT'
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                "completed": completed
            })
        })
            .then((response) => response.json())
            .then((data) => {
                ev.target.classList.toggle('checked');
            })
            .catch((error) => {
                console.error("Error:", error);
            });
    }
}, false);

// Create a new list item when clicking on the "Add" button
function newElement() {
    var li = document.createElement("li");
    var inputValue = document.getElementById("myInput").value;

    fetch("http://127.0.0.1:8000/todos", {
        method: "POST", // or 'PUT'
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "name": inputValue
        })
    })
        .then((response) => response.json())
        .then((data) => {
            li.appendChild(document.createTextNode(data.name));
            if (data.completed) {
                li.className = "checked"
            }
            document.getElementById("myInput").value = "";

            var span = document.createElement("SPAN");
            var txt = document.createTextNode("\u00D7");
            span.className = "close";
            span.appendChild(txt);
            span.onclick = function () {
                fetch(`http://127.0.0.1:8000/todos/${inputValue}`, {
                  method: "DELETE", // or 'PUT'
                  headers: {
                    "Content-Type": "application/json",
                  },
                })
                  .then((response) => response.json())
                  .then((data) => {
                    alert(data.message)
                    var div = this.parentElement;
                    div.style.display = "none";
                  })
                  .catch((error) => {
                    console.error("Error:", error);
                  });
            }
            li.appendChild(span);
            for (i = 0; i < close.length; i++) {
                close[i].onclick = function () {
                    var div = this.parentElement;
                    div.style.display = "none";
                }
            }
            const ul = document.getElementById('myUL');
            ul.appendChild(li)
        })
        .catch((error) => {
            console.error("Error:", error);
        });

}