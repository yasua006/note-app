/**
 * @param {NodeListOf<HTMLInputElement>} target_checkboxes
 */
const target_checkboxes = document.body
    .querySelector("main")
    .querySelectorAll("input[value='1'][type='checkbox']");
target_checkboxes.forEach((target_checkbox) => {
    const description_id = target_checkbox.parentElement.id.replaceAll("task-done-", "todo-description-");
    /**
     * @param {NodeListOf<HTMLHeadingElement>} target_descriptions
     */
    const target_descriptions = document.body
        .querySelector("main")
        .querySelectorAll(`li[id^=${description_id}]`);
    target_descriptions.forEach((target_desc) => {
        target_desc.style.fontWeight = "bold";
    });
});
