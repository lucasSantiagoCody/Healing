
function disabler(html_elements){
    for(html_element in html_elements){
        document.querySelector(html_elements[html_element]).disabled = 'true'
    }
}



