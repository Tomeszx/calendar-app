function check_required_fields(element) {
    var isValid = true
    $(element).parent().find("input[required], select[required]").each(function () {
        if ($(this).val() === "" || $(this).val() === null) {
            $(this).addClass("invalid");
            return isValid = false;
        } else {
            $(this).removeClass("invalid");
        }
    });
    return isValid;
}
