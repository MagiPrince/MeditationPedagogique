(function ($) {

var firstTimeTitle = true;
var firstTimeParagraph = true;


$(document).ready(function(){
    $('.modificationButton').click(function(e){
            //Check which button is up
            modifying = false
            if ($(this).hasClass("fa-edit") == true){
                modifying = true;
                //Hide ancient text;
                //$(this).parent().siblings('.modifiable').hide();
                // Not having 2 fields modifiying at the same time
                $(".modifiable").not($(this)).each(
                    function(){
                        if ($(this).siblings('.modification').find('.modificationButton').hasClass('fa-check-square')){
                            $(this).siblings('.modification').find('.modificationButton').toggleClass("fa-edit fa-check-square");
                        }
                    }
                )
            }
            $(this).toggleClass("fa-check-square fa-edit");
            classList = $(this).parent().siblings(".modifiable");
            if (classList.hasClass("title") && firstTimeTitle && modifying == true){
                $('.title').domEdit({
                    editorClass: 'titleModification',
                    onSetEditorStyle: function($editorTitle, $editingElement) {
                        $editorTitle.css('font-size', '150%');
                        $editorTitle.css('margin-left', '0%');
                    },
                    event: e,
                });
            }
            if (classList.hasClass("paragraph") && firstTimeParagraph && modifying == true){
                $('.paragraph').domEdit({
                    editorClass: 'paragraphModification',
                    onSetEditorStyle: function($editorParagraph, $editingElement) {
                        $editorParagraph.css('font-size', '90%');
                        $editorParagraph.css('margin-left', '3.6%');
                    },
                    event: e,
                });
            }
        })
});

    var editorId = 'dom-edit-' + Date.now();
    var editorHTML = '<textarea id="' + editorId + '"></textarea>';
    var $editor = $(editorHTML);
    var $currentTargetElement = null;

    function preventDefaultEvents(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function getTargetElementBoundingRect($aTargetElement) {
        var offset = $aTargetElement.offset();
        return {
            left: offset.left,
            top: offset.top,
            width: $aTargetElement.width(),
            height: $aTargetElement.height()
        };
    }


    function closeDomEditor(e) {
        if ($(this).hasClass("fa-edit") == true){
            $editor.remove();
            if ($currentTargetElement) {
                $currentTargetElement.html($editor.val());
                var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
                var result = String($editor.val());
                var url = "update-data/";
                if ($currentTargetElement[0].classList.contains("generalTitle")){
                    var field = "title";
                    var id = 0;
                    var table = "GeneralInformation"
                }
                else if ($currentTargetElement[0].classList.contains("generalDescription")){
                    var field = "description";
                    var id = 0;
                    var table = "GeneralInformation"
                }

                //Add modification in DB
                $.post(url,
                {
                    csrfmiddlewaretoken: CSRFtoken,
                    content : result,
                    table: table,
                    id: id,
                    field: field
                });
            }
            $currentTargetElement = null;
        }
    }

    function editorClick(e) {
        preventDefaultEvents(e);
    }

    function setEditorStyle($element, opts) {
        $editor.css(getTargetElementBoundingRect($element));
        $editor.css('font-size', $element.css('font-size'));
        $editor.css('font-weight', $element.css('font-weight'));
        $editor.css('text-align', $element.css('text-align'));
        $editor.css('font-family', $element.css('font-family'));
        //$editor.css('padding', $element.css('padding'));
        $editor.css('position', 'absolute');
        $editor.css('border-style', 'dotted');
        $editor.css('border-width', '3px');
        $editor.css('border-color', 'black');
        $editor.css('margin-top', '2%');
        $editor.css('outline', 'none');
        //$editor.css('min-width', '5%'); -> bien mais on ne peut plus valider

        if (opts && opts.onSetEditorStyle) {
            opts.onSetEditorStyle($editor, $element); //Add elements of css
        }
    }

    function setEditorState($element) {
        $editor.val($element.html());
        //$editor.select();
        //$editor.focus();
        $editor.click(editorClick);
        $editor.blur(closeDomEditor);
    }


    $.fn.domEdit = function (options) {
        var defaultOptions = {
            editorClass: ''
        }

        var opts = $.extend(defaultOptions, options);
        $editor.addClass(opts.editorClass);
        return this.each(function (idx, element) {
            preventDefaultEvents(opts.event);
            var target = $(element);
            var $body = $(document.body);

            if (target === $editor[0] || target === document.body || !$body.has(target)){
                return;
            }
            var $element = $(target);

            if (!$editor.parent().length) {
                $body.append($editor);
            }
            setEditorStyle($element, opts);
            setEditorState($element);
            $(element).siblings('.modification').find(".modificationButton").on('click', closeDomEditor);
            $currentTargetElement = $element;
        });
    }

})(jQuery);