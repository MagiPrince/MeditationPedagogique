function add_paragraph(lesson_number) {
    console.log('Boutton Add paragraph appuyé')
    order = 1 // TODO: Change this
    url = lesson_number + '/add_paragraph/' + order + '/'

    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    console.log(CSRFtoken);

    $.post(url,
        {
            csrfmiddlewaretoken: CSRFtoken,
        })
}
