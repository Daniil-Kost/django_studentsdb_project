//Journal JS
//------------------------------------
function initJournal(){
  var indicator =$('#ajax-progress-indicator');
  var err = $('#alert-danger');
  var info = $('#alert-warning');

	$('.day-box input[type="checkbox"]').click(function(event){
		var box =$(this);
		$.ajax(box.data('url'),{
			'type': 'POST',
			'async': true,
			'dataType': 'json',
			'data':{
				'pk': box.data('student-id'),
				'date': box.data('date'),
				'present': box.is(':checked') ? '1': '',
				'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
			},
      'beforeSend': function(xhr, settings){
        info.show();
        indicator.show();
        err.hide();
      },
			'error': function(xhr, status, error){
        info.hide();
        indicator.hide();
        err.show();
			},
			'success': function(data, status, xhr){
        info.show();
        indicator.hide();
        err.hide();
			}
		});
	});
}


//Students JS
//------------------------------------
function initAddStudentPage(){
  //a - tag <a>, student-add-form-link  - class in this tag
  $('a.student-add-form-link').click(function(event){
    var link =$(this);
    $.ajax({
      // передаем адресс на который надо сделать запрос
      'url': link.attr('href'),
      // тип данных с сервера
      'dataType': 'html',
      'type': 'get',
      'success': function(data, status, xhr){
        //check if we got successull response from the server
        if (status != 'success'){
          alert(gettext('There was an error on the server. Please try again a bit later.'));
          return false;
        }

        //update modal window with arrived content from the server
        // is id from base.html at tag <div>  in Modal Boilerplate
        var modal = $('#myModal'); 
        var html = $(data);
        // find() -method of search in html code
        var form = html.find('#ajax_form');
        console.log(html);
        modal.find('.modal-title').html(html.find(
          '#content-column h3').text());
        
        modal.find('.modal-body').html(form);

        //init our edit form
        initAddStudentForm(form, modal);

        //setup and show modal window finally
        //забороняэмо закривати вікно Escape
        //відключаємо фон позаду модального вікна
        modal.modal({
          //'keyboard': false,
          'backdrop': false,
          'show': true});
      },
      'error': function(){
        alert(gettext('There was an error on the server. Please try again a bit later.'));
        return false;
      }
    });

    return false;
  });

}

function initAddStudentForm(form, modal){
  //attach datepicker
  initDateFields();
  FormPhoto();

  //close modal window on Cancel button click
  form.find('input[name="student_cancel_button"]').click(function(event){
    //переменная modal взята из функции initEditStudentPage
    //в JS есть возможность использовать переменные 
    //обьявленные вне функции
    modal.modal('hide');
    return false;
  });

  //make form work in AJAX mode from jQuery Form
  form.ajaxForm({
    'dataType': 'html',
    'error': function(){
      alert(gettext('There was an error on the server. Please try again a bit later.'));
      return false;
    },
    'success': function(data, status, xhr){
      //делаем из html кода jquery обьект
      var html =$(data);
      var newform =html.find('#content-column form');

      //copy alert to modal window
      modal.find('.modal-body').html(html.find('.alert'));

      //copy form to modal if we found it in server response
      if (newform.length >0){
        modal.find('.modal-body').append(newform);

        //initialize form fields and buttons
        initAddStudentForm(newform, modal);
      }else{
        //if no form, it means success and we need to reload page
        //to get updated students list;
        //reload after 2 seconds, so that user can read
        //success message
        setTimeout(function(){location.reload(true);}, 500);
      }
    }
  });
}


//Groups JS
//------------------------------------
function initAddGroupPage(){
  //a - tag <a>, group-add-form-link  - class in this tag
  $('a.group-add-form-link').click(function(event){
    var link =$(this);
    $.ajax({
      // передаем адресс на который надо сделать запрос
      'url': link.attr('href'),
      // тип данных с сервера
      'dataType': 'html',
      'type': 'get',
      'success': function(data, status, xhr){
        //check if we got successull response from the server
        if (status != 'success'){
          alert(gettext('There was an error on the server. Please try again a bit later.'));
          return false;
        }

        //update modal window with arrived content from the server
        // is id from base.html at tag <div>  in Modal Boilerplate
        var modal = $('#myModal'); 
        var html = $(data);
        // find() -method of search in html code
        var form = html.find('#ajax_form');
        console.log(html);
        modal.find('.modal-title').html(html.find(
          '#content-column h3').text());
        
        modal.find('.modal-body').html(form);

        //init our edit form
        initAddGroupForm(form, modal);

        //setup and show modal window finally
        //забороняэмо закривати вікно Escape
        //відключаємо фон позаду модального вікна
        modal.modal({
          //'keyboard': false,
          'backdrop': false,
          'show': true});
      },
      'error': function(){
        alert(gettext('There was an error on the server. Please try again a bit later.'));
        return false;
      }
    });

    return false;
  });

}

function initAddGroupForm(form, modal){

  //close modal window on Cancel button click
  form.find('input[name="group_cancel_button"]').click(function(event){
    //переменная modal взята из функции initEditStudentPage
    //в JS есть возможность использовать переменные 
    //обьявленные вне функции
    modal.modal('hide');
    return false;
  });

 
  //make form work in AJAX mode from jQuery Form
  form.ajaxForm({
    'dataType': 'html',
    'error': function(){
      alert(gettext('There was an error on the server. Please try again a bit later.'));
      return false;
    },
    'success': function(data, status, xhr){
      //делаем из html кода jquery обьект
      var html =$(data);
      var newform =html.find('#content-column form');

      //copy alert to modal window
      modal.find('.modal-body').html(html.find('.alert'));

      //copy form to modal if we found it in server response
      if (newform.length >0){
        modal.find('.modal-body').append(newform);

        //initialize form fields and buttons
        initAddGroupForm(newform, modal);
      }else{
        //if no form, it means success and we need to reload page
        //to get updated students list;
        //reload after 2 seconds, so that user can read
        //success message
        setTimeout(function(){location.reload(true);}, 500);
      }
    }
  });
}


//Exams JS
//------------------------------------
function initAddExamPage(){
  //a - tag <a>, exam-add-form-link  - class in this tag
  $('a.exam-add-form-link').click(function(event){
    var link =$(this);
    $.ajax({
      // передаем адресс на который надо сделать запрос
      'url': link.attr('href'),
      // тип данных с сервера
      'dataType': 'html',
      'type': 'get',
      'success': function(data, status, xhr){
        //check if we got successull response from the server
        if (status != 'success'){
          alert(gettext('There was an error on the server. Please try again a bit later.'));
          return false;
        }

        //update modal window with arrived content from the server
        // is id from base.html at tag <div>  in Modal Boilerplate
        var modal = $('#myModal'); 
        var html = $(data);
        // find() -method of search in html code
        var form = html.find('#ajax_form');
        console.log(html);
        modal.find('.modal-title').html(html.find(
          '#content-column h3').text());
        
        modal.find('.modal-body').html(form);

        //init our edit form
        initAddExamForm(form, modal);

        //setup and show modal window finally
        //забороняэмо закривати вікно Escape
        //відключаємо фон позаду модального вікна
        modal.modal({
          //'keyboard': false,
          'backdrop': false,
          'show': true});
      },
      'error': function(){
        alert(gettext('There was an error on the server. Please try again a bit later.'));
        return false;
      }
    });

    return false;
  });

}

function initAddExamForm(form, modal){
  //attach datepicker
  initDateTimeFields();

  //close modal window on Cancel button click
  form.find('input[name="exam_cancel_button"]').click(function(event){
    //переменная modal взята из функции initEditStudentPage
    //в JS есть возможность использовать переменные 
    //обьявленные вне функции
    modal.modal('hide');
    return false;
  });


  //make form work in AJAX mode from jQuery Form
  form.ajaxForm({
    'dataType': 'html',
    'error': function(){
      alert(gettext('There was an error on the server. Please try again a bit later.'));
      return false;
    },
    'success': function(data, status, xhr){
      //делаем из html кода jquery обьект
      var html =$(data);
      var newform =html.find('#content-column form');

      //copy alert to modal window
      modal.find('.modal-body').html(html.find('.alert'));

      //copy form to modal if we found it in server response
      if (newform.length >0){
        modal.find('.modal-body').append(newform);

        //initialize form fields and buttons
        initAddExamForm(newform, modal);
      }else{
        //if no form, it means success and we need to reload page
        //to get updated students list;
        //reload after 2 seconds, so that user can read
        //success message
        setTimeout(function(){location.reload(true);}, 500);
      }
    }
  });
}


//Results JS
//------------------------------------
function initAddResultPage(){
  //a - tag <a>, result-add-form-link  - class in this tag
  $('a.result-add-form-link').click(function(event){
    var link =$(this);
    $.ajax({
      // передаем адресс на который надо сделать запрос
      'url': link.attr('href'),
      // тип данных с сервера
      'dataType': 'html',
      'type': 'get',
      'success': function(data, status, xhr){
        //check if we got successull response from the server
        if (status != 'success'){
          alert(gettext('There was an error on the server. Please try again a bit later.'));
          return false;
        }

        //update modal window with arrived content from the server
        // is id from base.html at tag <div>  in Modal Boilerplate
        var modal = $('#myModal'); 
        var html = $(data);
        // find() -method of search in html code
        var form = html.find('#ajax_form');
        console.log(html);
        modal.find('.modal-title').html(html.find(
          '#content-column h3').text());
        
        modal.find('.modal-body').html(form);

        //init our edit form
        initAddResultForm(form, modal);

        //setup and show modal window finally
        //забороняэмо закривати вікно Escape
        //відключаємо фон позаду модального вікна
        modal.modal({
          //'keyboard': false,
          'backdrop': false,
          'show': true});
      },
      'error': function(){
        alert(gettext('There was an error on the server. Please try again a bit later.'));
        return false;
      }
    });

    return false;
  });

}

function initAddResultForm(form, modal){
  //attach datepicker
  initDateTimeFields();

  //close modal window on Cancel button click
  form.find('input[name="result_cancel_button"]').click(function(event){
    //переменная modal взята из функции initEditStudentPage
    //в JS есть возможность использовать переменные 
    //обьявленные вне функции
    modal.modal('hide');
    return false;
  });


  //make form work in AJAX mode from jQuery Form
  form.ajaxForm({
    'dataType': 'html',
    'error': function(){
      alert(gettext('There was an error on the server. Please try again a bit later.'));
      return false;
    },
    'success': function(data, status, xhr){
      //делаем из html кода jquery обьект
      var html =$(data);
      var newform =html.find('#content-column form');

      //copy alert to modal window
      modal.find('.modal-body').html(html.find('.alert'));

      //copy form to modal if we found it in server response
      if (newform.length >0){
        modal.find('.modal-body').append(newform);

        //initialize form fields and buttons
        initAddResultForm(newform, modal);
      }else{
        //if no form, it means success and we need to reload page
        //to get updated students list;
        //reload after 2 seconds, so that user can read
        //success message
        setTimeout(function(){location.reload(true);}, 500);
      }
    }
  });
}


//11111111111111111111111111111111111111111111111111111111
//1111111111111111111111111111111111111111111111111111111111
//111111111111111111111111111111111111111111111111


//Code for different parts of application
//------------------------------------

function initEditModalPage(){
  //a - tag <a>, modal-edit-form-link  - class in this tag
  $('a.modal-edit-form-link').click(function(event){
    var link =$(this);
    $.ajax({
      // передаем адресс на который надо сделать запрос
      'url': link.attr('href'),
      // тип данных с сервера
      'dataType': 'html',
      'type': 'get',
      'success': function(data, status, xhr){
        //check if we got successull response from the server
        if (status != 'success'){
          alert(gettext('There was an error on the server. Please try again a bit later.'));
          return false;
        }

        //update modal window with arrived content from the server
        // is id from base.html at tag <div>  in Modal Boilerplate
        var modal = $('#myModal'); 
        var html = $(data);
        // find() -method of search in html code
        var form = html.find('#ajax_form');
        console.log(html);
        modal.find('.modal-title').html(html.find(
          '#content-column h3').text());
        
        modal.find('.modal-body').html(form);

        //init our edit form
        initEditModalForm(form, modal);

        //setup and show modal window finally
        //забороняэмо закривати вікно Escape
        //відключаємо фон позаду модального вікна
        modal.modal({
          //'keyboard': false,
          'backdrop': false,
          'show': true});
      },
      'error': function(){
        alert(gettext('There was an error on the server. Please try again a bit later.'));
        return false;
      }
    });

    return false;
  });

}

function initEditModalForm(form, modal){
  //attach datepicker
  initDateFields();
  initDateTimeFields();
  FormPhoto();
  
  //close modal window on Cancel button click
  form.find('input[name="cancel_button"]').click(function(event){
    //переменная modal взята из функции initEditStudentPage
    //в JS есть возможность использовать переменные 
    //обьявленные вне функции
    modal.modal('hide');
    return false;
  });

   //close modal window on Cancel button click
  form.find('button[name="cancel_button"]').click(function(event){
    //переменная modal взята из функции initEditStudentPage
    //в JS есть возможность использовать переменные 
    //обьявленные вне функции
    modal.modal('hide');
    return false;
  });

  //make form work in AJAX mode from jQuery Form
  form.ajaxForm({
    'dataType': 'html',
    'error': function(){
      alert(gettext('There was an error on the server. Please try again a bit later.'));
      return false;
    },
    'success': function(data, status, xhr){
      //делаем из html кода jquery обьект
      var html =$(data);
      var newform =html.find('#content-column form');

      //copy alert to modal window
      modal.find('.modal-body').html(html.find('.alert'));

      //copy form to modal if we found it in server response
      if (newform.length >0){
        modal.find('.modal-body').append(newform);

        //initialize form fields and buttons
        initEditModalForm(newform, modal);
      }else{
        //if no form, it means success and we need to reload page
        //to get updated students list;
        //reload after 2 seconds, so that user can read
        //success message
        setTimeout(function(){location.reload(true);}, 500);
      }
    }
  });
}


function initDeleteModalPage(){
  //a - tag <a>, student-edit-form-link  - class in this tag
  $('a.modal-delete-form-link').click(function(event){
    var link =$(this);
    $.ajax({
      // передаем адресс на который надо сделать запрос
      'url': link.attr('href'),
      // тип данных с сервера
      'dataType': 'html',
      'type': 'get',
      'success': function(data, status, xhr){
        //check if we got successull response from the server
        if (status != 'success'){
          alert(gettext('There was an error on the server. Please try again a bit later.'));
          return false;
        }

        //update modal window with arrived content from the server
        // is id from base.html at tag <div>  in Modal Boilerplate
        var modal = $('#myModal'); 
        var html = $(data);
        // find() -method of search in html code
        var form = html.find('#form-delete');
        console.log(html);
        modal.find('.modal-title').html(html.find(
          '#content-column h3').text());
        
        modal.find('.modal-body').html(form);

        //init our edit form
        initDeleteModalForm(form, modal);

        //setup and show modal window finally
        //забороняэмо закривати вікно Escape
        //відключаємо фон позаду модального вікна
        modal.modal({
          //'keyboard': false,
          'backdrop': false,
          'show': true});
      },
      'error': function(){
        alert(gettext('There was an error on the server. Please try again a bit later.'));
        return false;
      }
    });

    return false;
  });

}

function initDeleteModalForm(form, modal){

  //close modal window on Cancel button click
  form.find('input[name="cancel_button"]').click(function(event){
    //переменная modal взята из функции initEditStudentPage
    //в JS есть возможность использовать переменные 
    //обьявленные вне функции
    modal.modal('hide');
    return false;
  });

  //make form work in AJAX mode from jQuery Form
  form.ajaxForm({
    'dataType': 'html',
    'error': function(){
      alert(gettext('There was an error on the server. Please try again a bit later.'));
      return false;
    },
    'success': function(data, status, xhr){
      //делаем из html кода jquery обьект
      var html =$(data);
      var newform =html.find('#content-column form');

      //copy alert to modal window
      modal.find('.modal-body').html(html.find('.alert'));

      //copy form to modal if we found it in server response
      if (newform.length >0){
        modal.find('.modal-body').append(newform);

        //initialize form fields and buttons
        initDeleteModalForm(newform, modal);
      }else{
        //if no form, it means success and we need to reload page
        //to get updated students list;
        //reload after 2 seconds, so that user can read
        //success message
        setTimeout(function(){location.reload(true);}, 500);
      }
    }
  });
}


function initGroupSelector(){
  // look up select element with groups and attach our even handler
  // on field "change" event
  $('#group-selector select').change(function(event) {
    //get value of currently selected group option
    var group =$(this).val();

    if (group){
      //set cookie with expiration date 1 year since now;
      //cookie creation function takes period in days
      $.cookie('current_group', group, {'path': '/', 'expires': 365});
    }else{
      //otherwise we  delete the cookie
      $.removeCookie('current_group', {'path': '/'});
    }

    //and reload a page
    location.reload(true);

    return true;

  });
}

function initFormSelector(){
  $('#option-student-add').click(function(event) {
    document.location.href ='http://localhost:8000/students/add/';
  });
  $('#option-group-add').click(function(event) {
    document.location.href ='http://localhost:8000/groups/add/';
  });
  $('#option-exam-add').click(function(event) {
    document.location.href ='http://localhost:8000/exams/add/';
  });
  $('#option-result-add').click(function(event) {
    document.location.href ='http://localhost:8000/exams/results/add/';
  });

}

function initLangSelector() {
    $('#lang-selector select').change(function(event){
        var lan = $(this).val();
        if (lan) {
            $.cookie('django_language', lan, {'path': '/', 'expires': 365});
        } else {
            $.removeCookie('django_language', {'path': '/'});
        }
        location.reload(true);
        return true;
     });
}

function initDateFields(){
//find class dateinput in HTML code and set function with plagin
//set function datetimepicker with plagin 
  $('input.dateinput').datetimepicker({ 
    'format': 'YYYY-MM-DD',
    locale: 'uk',
    dayViewHeaderFormat: 'MMM YYYY',
  }).on('dp.hide', function(event){
    $(this).blur();
  });

}

function initDateTimeFields(){
//find class dateinput in HTML code
//set function datetimepicker with plagin 
  $('input.datetimeinput').datetimepicker({
    'format': 'YYYY-MM-DD hh:mm',
    locale: 'uk',
    dayViewHeaderFormat: 'MMM YYYY',
  }).on('dp.hide', function(event){
    $(this).blur();
  });
}

function FormPhotoPage(){
  var photo = $('#div_id_photo').find('div.controls');
  var photolink = $(photo).find('a').attr('href');
    if (photolink == undefined) {
            photolink = "/static/image/avatar.png";
    }
    var htmltext = "<img class='img-circle' src='"+photolink+"' height='150' width='150' /> \
<br><br><br><br><br><br><br><br><input id='id_photo' class='clearablefileinput' align='left' type='file' name='photo'> \
<input id='photo-clear_id' type='checkbox' name='photo-clear'> <label id='photo-clear_id'>Очистити</label>";
    photo.html(htmltext);
}

function FormPhoto(){
  var photo = $('#div_id_photo').find('div.controls');
  var photolink = $(photo).find('a').attr('href');
    if (photolink == undefined) {
            photolink = "/static/image/avatar.png";
    }
    var htmltext = "<img class='img-circle' id='f_img' src='"+photolink+"' height='100' width='100' /> \
<br><input id='id_photo' class='clearablefileinput' align='left' type='file' name='photo'> \
<label id='photo-clear_id'>Очистити</label><input id='photo-clear_id' type='checkbox' name='photo-clear'>";
    photo.html(htmltext);
}

function initCancelButton(){
  //students
  $('#submit-id-student_cancel_button').click(function(event){
    document.location.href ='http://localhost:8000/';
  });
  //groups
  $('#submit-id-group_cancel_button').click(function(event){
    document.location.href ='http://localhost:8000/groups/';
  });
  //exams
  $('#submit-id-exam_cancel_button').click(function(event){
    document.location.href ='http://localhost:8000/exams/';
  });
  //results
  $('#submit-id-result_cancel_button').click(function(event){
    document.location.href ='http://localhost:8000/exams/results/';
  });
  //login-registration
  $('#submit-id-login_cancel_button').click(function(event){
    document.location.href ='http://localhost:8000/';
  });
  //users
  $('#submit-id-user_cancel_button').click(function(event){
    document.location.href ='http://localhost:8000/accounts/users';
  });
}


$(document).ready(function(){
	initJournal();

  initGroupSelector();
  initFormSelector();
  initLangSelector();
  initDateFields();
  initCancelButton();
  initEditModalPage();
  initDeleteModalPage();
  FormPhotoPage();
  initDateTimeFields();

  initAddStudentPage();
  initAddGroupPage();
  initAddExamPage();
  initAddResultPage();
});