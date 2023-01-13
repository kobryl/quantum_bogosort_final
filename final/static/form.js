const stops = JSON.parse(document.getElementById("stops-data").textContent);
const minCharacters = 2;


window.addEventListener("load", function(){
    function autocompleteField(nameField, idField) {
        let currentlyFocusedStop;

        nameField.addEventListener("input", function(e){
            let value = this.value;
            if (!value) return false;
    
            closeOtherLists(nameField.parentNode);

            if (value.length >= minCharacters) {
                currentlyFocusedStop = -1;
                let stopList = document.createElement("div");
                stopList.setAttribute("id", nameField.id + "-list");
                stopList.setAttribute("class", "stop-list");
                nameField.parentNode.appendChild(stopList);
    
                for (let i = 0; i < stops.length; i++) {
                    let stopName = stops[i].fields.stopName + " " + stops[i].fields.subName;
                    if (stopName.substring(0, value.length).toLowerCase() == value.toLowerCase()) {
                        let stopElement = document.createElement("div");
                        stopElement.setAttribute("class", "stop-element");
                        stopElement.innerHTML = "<span class='stop-match'>" + stopName.substring(0, value.length) + "</span>";
                        stopElement.innerHTML += stopName.substring(value.length);
                        stopElement.innerHTML += "<input type='hidden' value='" + stops[i].pk + "'>";
                        stopElement.addEventListener("click", function(e) {
                            nameField.value = stopName;
                            idField.value = stops[i].pk;
                            closeOtherLists(null);
                        });
                        stopList.appendChild(stopElement);
                    }
                }
            }
        });

        nameField.addEventListener("keydown", function(e){
            if (document.getElementById(nameField.id + "-list")) {
                let stopList = document.getElementById(nameField.id + "-list");
                let currentElements = stopList.querySelectorAll("div");
                if (e.keyCode == 40) {      // down arrow key
                    currentlyFocusedStop++;
                    setActive(currentElements);
                }
                else if (e.keyCode == 38) {     // up arrow key
                    currentlyFocusedStop--;
                    setActive(currentElements);
                }
                else if (e.keyCode == 13) {     // enter key
                    e.preventDefault();
                    if (currentlyFocusedStop > -1) {
                        currentElements[currentlyFocusedStop].click();
                    }
                }
            }
        });


        function setActive(elements) {
            if (!elements) return false;

            for (let i = 0; i < elements.length; i++) {
                elements[i].classList.remove("autocomplete-active");
            }

            if (currentlyFocusedStop >= elements.length) currentlyFocusedStop = elements.length - 1;
            if (currentlyFocusedStop < 0) currentlyFocusedStop = 0;
            elements[currentlyFocusedStop].classList.add("autocomplete-active");
        }
    }


    function closeOtherLists(element) {
        let lists = document.querySelectorAll(".stop-list");
        for (let i = 0; i < lists.length; i++) {
            if (element != null) {
                if (element != lists[i]) {
                    lists[i].parentNode.removeChild(lists[i]);
                }
            } 
            else {
                lists[i].parentNode.removeChild(lists[i]);
            }
        }
    }


    document.addEventListener("click", function (e) {
        closeOtherLists(e.target);
    });


    let items = document.querySelectorAll(".autocomplete-item");
    for (let i = 0; i < items.length; i++) {
        let nameField = items[i].querySelector(".autocomplete-name");
        let idField = items[i].querySelector(".autocomplete-id");
        nameField.value = "";
        idField.value = "";
        autocompleteField(nameField, idField);
    }
});