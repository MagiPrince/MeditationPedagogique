/*$(document).ready(function(){
    $('.modificationButton').click(function(e){
        //Check which button is up

        var modifying = false;
        if ($(this).hasClass("fa-edit")){
            $(this).removeClass("fa-edit");
            $(this).addClass("fa-check-square");
            modifying = true;
        }
        else{
            $(this).addClass("fa-edit");
            $(this).removeClass("fa-check-square");
            modifying = false;
        }
        classList = $(this).parent().siblings(".modifiable")
        if (classList.hasClass("titre") && modifying){
            $('.titre').domEdit({
                editorClass: 'titreModification',
                onSetEditorStyle: function($editorTitre, $editingElement) {
                    $editorTitre.css('font-size', '150%');
                    $editorTitre.css('margin-left', '0%');
                },
                event: e
            });
        }
        if (classList.hasClass("introduction") && modifying){
            $('.introduction').domEdit({
                editorClass: 'introductionModification',
                onSetEditorStyle: function($editorIntro, $editingElement) {
                    $editorIntro.css('font-size', '90%');
                    $editorIntro.css('margin-left', '3.6%');
                },
                event: e
            });
        }
        
    });
});*/