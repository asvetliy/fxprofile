wizard = {
  initMaterialTransferWizard: function () {
    // Code for the Validator
    let $validator = $('.card-wizard form').validate({
      rules: {
        transfer_type: {
          required: true
        },
        amount: {
          required: true,
          min: 0.01,
          number: true
        },
        from_personal_account: {
          required: true
        },
        from_trading_account: {
          required: true
        },
        to_personal_account: {
          required: true
        },
        to_trading_account: {
          required: true
        }
      },
      highlight: function (element) {
        $(element).closest('.form-group').removeClass('has-success').addClass('has-danger');
      },
      success: function (label, element) {
        $(element).closest('.form-group').removeClass('has-danger').addClass('has-success');
        label.parent().removeClass('error');
        label.remove();
      },
      errorPlacement: function (error, element) {
        $(element).closest('.form-group').append(error);
      }
    });

    $("#from_personal_account").change(function () {
      $('.card-wizard form').valid();
      let from_currency = $(this).children('option:selected').attr('currency');
      $('#to_trading_account > option').each(function () {
        let to_currency = $(this).attr('currency');
        if (to_currency === from_currency) {
          $(this).attr('disabled', false);
        } else {
          $(this).attr('disabled', true);
        }
      });
    });

    $("#from_trading_account").change(function () {
      $('.card-wizard form').valid();
      let from_currency = $(this).children('option:selected').attr('currency');
      $('#to_personal_account > option').each(function () {
        let to_currency = $(this).attr('currency');
        if (to_currency === from_currency) {
          $(this).attr('disabled', false);
        } else {
          $(this).attr('disabled', true);
        }
      });
    });

    $("#transfer_type").change(function () {
      $('.card-wizard form').valid();
      let transfer_type = $(this).val();
      if (transfer_type === "pt") {
        $("#from_trading_account_block").addClass("d-none");
        $("#from_personal_account_block").removeClass("d-none");
        $("#to_personal_account_block").addClass("d-none");
        $("#to_trading_account_block").removeClass("d-none");
      } else if (transfer_type === "tp") {
        $("#from_personal_account_block").addClass("d-none");
        $("#from_trading_account_block").removeClass("d-none");
        $("#to_trading_account_block").addClass("d-none");
        $("#to_personal_account_block").removeClass("d-none");
      }

    });

    $('.btn-finish').click(function () {
      $(this).attr('disabled', true);
      $(this).addClass('disabled');
      if ($('.card-wizard form').valid()) {
        $('form').submit();
      } else {
        $(this).attr('disabled', false);
        $(this).removeClass('disabled');
      }
    });

    // Wizard Initialization
    $('.card-wizard').bootstrapWizard({
      'tabClass': 'nav nav-pills',
      'nextSelector': '.btn-next',
      'previousSelector': '.btn-previous',

      onNext: function (tab, navigation, index) {
        if (!$('.card-wizard form').valid()) {
          $validator.focusInvalid();
          return false;
        }
      },

      onInit: function (tab, navigation, index) {
        //check number of tabs and fill the entire row
        let $total = navigation.find('li').length;
        let $wizard = navigation.closest('.card-wizard');

        let $first_li = navigation.find('li:first-child a').html();
        let $moving_div = $('<div class="moving-tab">' + $first_li + '</div>');
        $('.card-wizard .wizard-navigation').append($moving_div);

        refreshAnimation($wizard, index);

        $('.moving-tab').css('transition', 'transform 0s');
      },

      onTabClick: function (tab, navigation, index) {
        return $('.card-wizard form').valid();
      },

      onTabShow: function (tab, navigation, index) {
        let $total = navigation.find('li').length;
        let $current = index + 1;

        let $wizard = navigation.closest('.card-wizard');

        // If it's the last tab then hide the last button and show the finish instead
        if ($current >= $total) {
          $($wizard).find('.btn-next').hide();
          $($wizard).find('.btn-finish').show();
        } else {
          $($wizard).find('.btn-next').show();
          $($wizard).find('.btn-finish').hide();
        }

        let button_text = navigation.find('li:nth-child(' + $current + ') a').html();

        setTimeout(function () {
          $('.moving-tab').text(button_text);
        }, 150);

        let checkbox = $('.footer-checkbox');

        if (!index === 0) {
          $(checkbox).css({
            'opacity': '0',
            'visibility': 'hidden',
            'position': 'absolute'
          });
        } else {
          $(checkbox).css({
            'opacity': '1',
            'visibility': 'visible'
          });
        }

        refreshAnimation($wizard, index);
      }
    });

    $('.set-full-height').css('height', 'auto');

    $(window).resize(function () {
      $('.card-wizard').each(function () {
        let $wizard = $(this);

        let index = $wizard.bootstrapWizard('currentIndex');
        refreshAnimation($wizard, index);

        $('.moving-tab').css({
          'transition': 'transform 0s'
        });
      });
    });

    function refreshAnimation($wizard, index) {
      let $total = $wizard.find('.nav li').length;
      let $li_width = 100 / $total;

      let total_steps = $wizard.find('.nav li').length;
      let move_distance = $wizard.width() / total_steps;
      let index_temp = index;
      let vertical_level = 0;

      let mobile_device = $(document).width() < 600 && $total > 3;

      if (mobile_device) {
        move_distance = $wizard.width() / 2;
        index_temp = index % 2;
        $li_width = 50;
      }

      $wizard.find('.nav li').css('width', $li_width + '%');

      let step_width = move_distance;
      move_distance = move_distance * index_temp;

      let $current = index + 1;

      if ($current === 1 || (mobile_device === true && (index % 2 === 0))) {
        move_distance -= 8;
      } else if ($current === total_steps || (mobile_device === true && (index % 2 === 1))) {
        move_distance += 8;
      }

      if (mobile_device) {
        vertical_level = parseInt(index / 2);
        vertical_level = vertical_level * 38;
      }

      $wizard.find('.moving-tab').css('width', step_width);
      $('.moving-tab').css({
        'transform': 'translate3d(' + move_distance + 'px, ' + vertical_level + 'px, 0)',
        'transition': 'all 0.5s cubic-bezier(0.29, 1.42, 0.79, 1)'

      });
    }
  },
  initMaterialDepositWizard: function () {
    // Code for the Validator
    let $validator = $('.card-wizard form').validate({
      rules: {
        amount: {
          required: true,
          min: 0.01,
          number: true
        },
        account: {
          required: true
        },
        payment_system: {
          required: true
        },
        terms: {
          required: true
        }
      },

      highlight: function (element) {
        $(element).closest('.form-group').removeClass('has-success').addClass('has-danger');
      },
      success: function (label, element) {
        $(element).closest('.form-group').removeClass('has-danger').addClass('has-success');
        label.parent().removeClass('error');
        label.remove();
      },
      errorPlacement: function (error, element) {
        $(element).closest('.form-group').append(error);
      }
    });


    // Wizard Initialization
    $('.card-wizard').bootstrapWizard({
      'tabClass': 'nav nav-pills',
      'nextSelector': '.btn-next',
      'previousSelector': '.btn-previous',

      onNext: function (tab, navigation, index) {
        let $valid = $('.card-wizard form').valid();
        if (!$valid) {
          $validator.focusInvalid();
          return false;
        }
      },

      onInit: function (tab, navigation, index) {
        //check number of tabs and fill the entire row
        let $total = navigation.find('li').length;
        let $wizard = navigation.closest('.card-wizard');

        let $first_li = navigation.find('li:first-child a').html();
        let $moving_div = $('<div class="moving-tab">' + $first_li + '</div>');
        $('.card-wizard .wizard-navigation').append($moving_div);

        refreshAnimation($wizard, index);

        $('.moving-tab').css('transition', 'transform 0s');
      },

      onTabClick: function (tab, navigation, index) {
        return $('.card-wizard form').valid();
      },

      onTabShow: function (tab, navigation, index) {
        let $total = navigation.find('li').length;
        let $current = index + 1;

        let $wizard = navigation.closest('.card-wizard');

        // If it's the last tab then hide the last button and show the finish instead
        if ($current >= $total) {
          $($wizard).find('.btn-next').hide();
          $($wizard).find('.btn-finish').show();
        } else {
          $($wizard).find('.btn-next').show();
          $($wizard).find('.btn-finish').hide();
        }

        let button_text = navigation.find('li:nth-child(' + $current + ') a').html();

        setTimeout(function () {
          $('.moving-tab').text(button_text);
        }, 150);

        let checkbox = $('.footer-checkbox');

        if (!index == 0) {
          $(checkbox).css({
            'opacity': '0',
            'visibility': 'hidden',
            'position': 'absolute'
          });
        } else {
          $(checkbox).css({
            'opacity': '1',
            'visibility': 'visible'
          });
        }

        refreshAnimation($wizard, index);
      }
    });

    // Prepare the preview for profile picture
    $("#wizard-picture").change(function () {
      readURL(this);
    });

    $('[data-toggle="wizard-radio"]').click(function () {
      let wizard = $(this).closest('.card-wizard');
      wizard.find('[data-toggle="wizard-radio"]').removeClass('active');
      $(this).addClass('active');
      $(wizard).find('[type="radio"]').removeAttr('checked');
      $(this).find('[type="radio"]').attr('checked', 'true');
    });

    $('[data-toggle="wizard-checkbox"]').click(function () {
      if ($(this).hasClass('active')) {
        $(this).removeClass('active');
        $(this).find('[type="checkbox"]').removeAttr('checked');
      } else {
        $(this).addClass('active');
        $(this).find('[type="checkbox"]').attr('checked', 'true');
      }
    });

    $('#deposit-btn').click(function () {
      $(this).attr('disabled', true);
      let ps = $('#payment_system').val();
      if (ps) {
        let lang = $('html').attr('lang');
        let url = '';
        let $f = $('form');
        if (lang !== 'en') {
          url = '/' + lang + '/payments/' + ps + '/init';
        } else {
          url = '/payments/' + ps + '/init';
        }
        $f.attr('action', url);
        $f.submit();
      } else {
        $(this).attr('disabled', false);
      }
    });

    $('.set-full-height').css('height', 'auto');

    $(window).resize(function () {
      $('.card-wizard').each(function () {
        let $wizard = $(this);

        let index = $wizard.bootstrapWizard('currentIndex');
        refreshAnimation($wizard, index);

        $('.moving-tab').css({
          'transition': 'transform 0s'
        });
      });
    });

    function readURL(input) {
      if (input.files && input.files[0]) {
        let reader = new FileReader();

        reader.onload = function (e) {
          $('#wizardPicturePreview').attr('src', e.target.result).fadeIn('slow');
        };
        reader.readAsDataURL(input.files[0]);
      }
    }

    function refreshAnimation($wizard, index) {
      let $total = $wizard.find('.nav li').length;
      let $li_width = 100 / $total;

      let total_steps = $wizard.find('.nav li').length;
      let move_distance = $wizard.width() / total_steps;
      let index_temp = index;
      let vertical_level = 0;

      let mobile_device = $(document).width() < 600 && $total > 3;

      if (mobile_device) {
        move_distance = $wizard.width() / 2;
        index_temp = index % 2;
        $li_width = 50;
      }

      $wizard.find('.nav li').css('width', $li_width + '%');

      let step_width = move_distance;
      move_distance = move_distance * index_temp;

      let $current = index + 1;

      if ($current === 1 || (mobile_device === true && (index % 2 === 0))) {
        move_distance -= 8;
      } else if ($current === total_steps || (mobile_device === true && (index % 2 === 1))) {
        move_distance += 8;
      }

      if (mobile_device) {
        vertical_level = parseInt((index / 2).toString());
        vertical_level = vertical_level * 38;
      }

      $wizard.find('.moving-tab').css('width', step_width);
      $('.moving-tab').css({
        'transform': 'translate3d(' + move_distance + 'px, ' + vertical_level + 'px, 0)',
        'transition': 'all 0.5s cubic-bezier(0.29, 1.42, 0.79, 1)'

      });
    }
  },
  initMaterialWithdrawWizard: function () {
    // Code for the Validator
    let $validator = $('.card-wizard form').validate({
      rules: {
        amount: {
          required: true,
          min: 0.01,
          number: true
        },
        account: {
          required: true
        },
        payment_system: {
          required: true
        },
      },

      highlight: function (element) {
        $(element).closest('.form-group').removeClass('has-success').addClass('has-danger');
      },
      success: function (label, element) {
        $(element).closest('.form-group').removeClass('has-danger').addClass('has-success');
        label.parent().removeClass('error');
        label.remove();
      },
      errorPlacement: function (error, element) {
        $(element).closest('.form-group').append(error);
      }
    });


    // Wizard Initialization
    $('.card-wizard').bootstrapWizard({
      'tabClass': 'nav nav-pills',
      'nextSelector': '.btn-next',
      'previousSelector': '.btn-previous',

      onNext: function (tab, navigation, index) {
        let $valid = $('.card-wizard form').valid();
        if (!$valid) {
          $validator.focusInvalid();
          return false;
        }
      },

      onInit: function (tab, navigation, index) {
        //check number of tabs and fill the entire row
        let $total = navigation.find('li').length;
        let $wizard = navigation.closest('.card-wizard');

        let $first_li = navigation.find('li:first-child a').html();
        let $moving_div = $('<div class="moving-tab">' + $first_li + '</div>');
        $('.card-wizard .wizard-navigation').append($moving_div);

        refreshAnimation($wizard, index);

        $('.moving-tab').css('transition', 'transform 0s');
      },

      onTabClick: function (tab, navigation, index) {
        return $('.card-wizard form').valid();
      },

      onTabShow: function (tab, navigation, index) {
        let $total = navigation.find('li').length;
        let $current = index + 1;

        let $wizard = navigation.closest('.card-wizard');

        // If it's the last tab then hide the last button and show the finish instead
        if ($current >= $total) {
          $($wizard).find('.btn-next').hide();
          $($wizard).find('.btn-finish').show();
        } else {
          $($wizard).find('.btn-next').show();
          $($wizard).find('.btn-finish').hide();
        }

        let button_text = navigation.find('li:nth-child(' + $current + ') a').html();

        setTimeout(function () {
          $('.moving-tab').text(button_text);
        }, 150);

        let checkbox = $('.footer-checkbox');

        if (!index === 0) {
          $(checkbox).css({
            'opacity': '0',
            'visibility': 'hidden',
            'position': 'absolute'
          });
        } else {
          $(checkbox).css({
            'opacity': '1',
            'visibility': 'visible'
          });
        }

        refreshAnimation($wizard, index);
      }
    });


    // Prepare the preview for profile picture
    $("#wizard-picture").change(function () {
      readURL(this);
    });

    $('[data-toggle="wizard-radio"]').click(function () {
      let wizard = $(this).closest('.card-wizard');
      wizard.find('[data-toggle="wizard-radio"]').removeClass('active');
      $(this).addClass('active');
      $(wizard).find('[type="radio"]').removeAttr('checked');
      $(this).find('[type="radio"]').attr('checked', 'true');
    });

    $('[data-toggle="wizard-checkbox"]').click(function () {
      if ($(this).hasClass('active')) {
        $(this).removeClass('active');
        $(this).find('[type="checkbox"]').removeAttr('checked');
      } else {
        $(this).addClass('active');
        $(this).find('[type="checkbox"]').attr('checked', 'true');
      }
    });

    $('.btn-finish').click(function () {
      $(this).attr('disabled', true);
      $(this).addClass('disabled');
      if ($('.card-wizard form').valid()) {
        $('form').submit();
      } else {
        $(this).attr('disabled', false);
        $(this).removeClass('disabled');
      }
    });

    $('.set-full-height').css('height', 'auto');

    $(window).resize(function () {
      $('.card-wizard').each(function () {
        let $wizard = $(this);

        let index = $wizard.bootstrapWizard('currentIndex');
        refreshAnimation($wizard, index);

        $('.moving-tab').css({
          'transition': 'transform 0s'
        });
      });
    });

    function readURL(input) {
      if (input.files && input.files[0]) {
        let reader = new FileReader();

        reader.onload = function (e) {
          $('#wizardPicturePreview').attr('src', e.target.result).fadeIn('slow');
        };
        reader.readAsDataURL(input.files[0]);
      }
    }

    function refreshAnimation($wizard, index) {
      let $total = $wizard.find('.nav li').length;
      let $li_width = 100 / $total;

      let total_steps = $wizard.find('.nav li').length;
      let move_distance = $wizard.width() / total_steps;
      let index_temp = index;
      let vertical_level = 0;

      let mobile_device = $(document).width() < 600 && $total > 3;

      if (mobile_device) {
        move_distance = $wizard.width() / 2;
        index_temp = index % 2;
        $li_width = 50;
      }

      $wizard.find('.nav li').css('width', $li_width + '%');

      let step_width = move_distance;
      move_distance = move_distance * index_temp;

      let $current = index + 1;

      if ($current === 1 || (mobile_device === true && (index % 2 === 0))) {
        move_distance -= 8;
      } else if ($current === total_steps || (mobile_device === true && (index % 2 === 1))) {
        move_distance += 8;
      }

      if (mobile_device) {
        vertical_level = parseInt((index / 2).toString());
        vertical_level = vertical_level * 38;
      }

      $wizard.find('.moving-tab').css('width', step_width);
      $('.moving-tab').css({
        'transform': 'translate3d(' + move_distance + 'px, ' + vertical_level + 'px, 0)',
        'transition': 'all 0.5s cubic-bezier(0.29, 1.42, 0.79, 1)'

      });
    }
  }
};
