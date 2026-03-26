import { main_elem } from "./modules/main_elem_var.js";
const target_checkboxes = main_elem.querySelectorAll("input[value='1'][type='checkbox']");
target_checkboxes.forEach((target_checkbox) => {
    const description_id = target_checkbox.id.replaceAll("task-done-", "todo-description-");
    const target_descriptions = main_elem.querySelectorAll(`p[id^=${description_id}]`);
    target_descriptions.forEach((target_desc) => {
        target_desc.style.textDecoration = "line-through";
    });
});
