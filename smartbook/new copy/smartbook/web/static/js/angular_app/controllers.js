function validateEmail(email) { 
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}

add_new_customer = function($http, $scope) { 
    if($scope.customer_name == '') {
        $scope.error_message = "Please enter customer name";
        $scope.error_flag = true;
    } else if($scope.email_id == '') {
        $scope.error_message = "Please enter email";
        $scope.error_flag = true;
    } else if(!validateEmail($scope.email_id)){
        $scope.error_message = "Please enter correct email";
        $scope.error_flag = true;
    }else {
        params = { 
            'name':$scope.customer_name,
            'house': $scope.house_name,
            'street': $scope.street,
            'city': $scope.city,
            'district':$scope.district,
            'pin': $scope.pin,
            'mobile': $scope.mobile,
            'phone': $scope.land_line,
            'email': $scope.email_id,
            "csrfmiddlewaretoken" : $scope.csrf_token
        }
        $http({
            method : 'post',
            url : "/create_customer/",
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data, status) {
            
            if (data.result == 'error'){
                $scope.error_flag=true;
                $scope.message = data.message;
            } else {
                $scope.popup.hide_popup();
                $scope.get_customers();
            }
        }).error(function(data, success){
            
        });
    } 
}       
get_quotation_details = function($http, $scope){

    var ref_no = $scope.quotation_no;
    $scope.quotations = []
    $http.get('/sales/quotation_details/?reference_no='+ref_no+'&sales_invoice=true').success(function(data)
    {
        console.log(data.quotations.length);
        if(data.quotations.length > 0){
            $scope.selecting_quotation = true;
            $scope.quotation_selected = false;
            $scope.quotations = data.quotations;
        } else {
            $scope.message = "There is no quotations with this number";
        }
        
    }).error(function(data, status)
    {
        console.log(data || "Request failed");
    });
}


function ExpenseController($scope, $element, $http, $timeout, $location) {

	$scope.expense_heads = [];
	$scope.expense_head = '';
    $scope.payment_mode = 'cash';
    $scope.payment_mode_selection = true;
    $scope.voucher_no = '';
    $scope.is_valid = false;
    $scope.error_flag = false;
    $scope.error_message = '';

	$scope.init = function(csrf_token)
    {
        $scope.csrf_token = csrf_token;
        $scope.get_expense_head_list();
        
    }
    $scope.get_expense_head_list = function() {
    	$http.get('/expenses/expense_head_list/').success(function(data)
        {
        	$scope.expense_heads = data.expense_heads;
            $scope.expense_head = 'select';
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.payment_mode_change = function(payment_mode) {
        if(payment_mode == 'cheque') {
            $scope.payment_mode_selection = false;
            
            new Picker.Date($$('#cheque_date'), {
                timePicker: false,
                positionOffset: {x: 5, y: 0},
                pickerClass: 'datepicker_bootstrap',
                useFadeInOut: !Browser.ie,
                format:'%d/%m/%Y',
            });
        } else {
            $scope.payment_mode_selection = true;
        }
    }
    $scope.reset = function() {
        $scope.expense_head = 'select';
        $scope.amount = '';
        $scope.payment_mode = 'cash';
        $scope.payment_mode_selection = true;
        $scope.narration = '';
        $scope.cheque_no = '';
        $scope.cheque_date = '';
        $scope.branch = '';
        $scope.bank_name = '';
        $scope.cheque_date = $$('#cheque_date').set('value', '');
    }
    $scope.form_validation = function(){
        $scope.voucher_no = $$('#voucher_no')[0].get('value');
        $scope.date = $$('#date')[0].get('value');
        $scope.cheque_date = $$('#cheque_date')[0].get('value');
        if ($scope.expense_head == '' || $scope.expense_head == undefined || $scope.expense_head == 'select') {
            $scope.error_flag = true;
            $scope.error_message = 'Please choose expense head';
            return false;
        } else if ($scope.amount == '' || $scope.amount == undefined) {
            $scope.error_flag = true;
            $scope.error_message = 'Please enter amount';
            return false;
        } else if ($scope.narration == '' || $scope.narration == undefined) {
            $scope.error_flag = true;
            $scope.error_message = 'Please add narration';
            return false;
        } else if( $scope.payment_mode == 'cheque' && ($scope.cheque_no == '' || $scope.cheque_no == undefined)) {
            $scope.error_flag = true;
            $scope.error_message = 'Please add cheque no';
            return false;
        } else if( $scope.payment_mode == 'cheque' && ($scope.cheque_date == '' || $scope.cheque_date == undefined)) {
            $scope.error_flag = true;
            $scope.error_message = 'Please add cheque date';
            return false;
        } else if( $scope.payment_mode == 'cheque' && ($scope.bank_name == '' || $scope.bank_name == undefined)) {
            $scope.error_flag = true;
            $scope.error_message = 'Please add bank name';
            return false;
        } else if( $scope.payment_mode == 'cheque' && ($scope.branch == '' || $scope.branch == undefined)) {
            $scope.error_flag = true;
            $scope.error_message = 'Please add branch';
            return false;
        }
        return true;
    }
    $scope.save_expense = function(){
        $scope.is_valid = $scope.form_validation();
        if ($scope.is_valid) {
            $scope.error_flag = false;
            $scope.error_message = '';
            params = { 
                'voucher_no':$scope.voucher_no,
                'date': $scope.date,
                'head_name': $scope.expense_head,
                'amount': $scope.amount,
                'payment_mode': $scope.payment_mode,
                'cheque_date':$scope.cheque_date,
                'cheque_no': $scope.cheque_no,
                'bank_name': $scope.bank_name,
                'branch': $scope.branch,
                'narration': $scope.narration,
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/expenses/new_expense/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                
                if (data.result == 'error'){
                    $scope.error_flag=true;
                    $scope.message = data.message;
                } else {
                    $scope.error_flag=false;
                    $scope.message = '';
                    document.location.href ='/expenses/new_expense/';
                }
            }).error(function(data, status){
                console.log(data);
            });
        }
    }
}

function AddEditUserController($scope, $element, $http, $timeout, $location) {
    $scope.init = function(csrf_token, user_type, salesman)
    {
        $scope.popup = '';
        $scope.new_designation = '';
        $scope.csrf_token = csrf_token;
        $scope.user_type = user_type;
        // $scope.new_desiganation_flag = true;
        $scope.error_flag = true;
        $scope.designation_flag = false;
        $scope.message = '';
        $scope.designation = salesman;
        if ($scope.user_type == 'staff'){
            $scope.get_designation_list();
            $scope.designation = salesman;
        } 
    }

    $scope.get_designation_list = function() {
        $http.get('/designation_list/').success(function(data)
        {
            $scope.designations = data.designations;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.add_designation = function() {
        if($scope.designation == 'other') {
            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '27%',
                'message_padding': '0px',
                'left': '28%',
                'top': '175px',
                'height': '115px',
                'content_div': '#add_designation'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
            // $scope.new_desiganation_flag = false;
        }
    }
    $scope.validate = function() {

    }
    $scope.add_new_designation = function() {
        params = { 
            'new_designation':$scope.new_designation,
            "csrfmiddlewaretoken" : $scope.csrf_token
        }
        $http({
            method : 'post',
            url : "/add_designation/",
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data, status) {
            
            if (data.result == 'error'){
                $scope.error_flag=true;
                $scope.message = data.message;
            } else {
                $scope.error_flag=false;
                $scope.message = '';
                $scope.popup.hide_popup();
                $scope.get_designation_list();
                $scope.designation = $scope.new_designation;
                // $scope.new_desiganation_flag = true;
            }
        }).error(function(data, success){
            
        });
    }
    $scope.show_designation_list = function() {
        $scope.designation_flag = true;
        $('#designation_val').hide();
        $scope.designation = $('#designation_val').val();
    }
    $scope.selected_head = function(head_name) {
    	$scope.expense_head = head_name;
    }
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }
	
}

function PurchaseController($scope, $element, $http, $timeout, share, $location) {

    $scope.items = [];
    $scope.selected_item = '';
    $scope.vendor_name = '';
    $scope.brand_name = '';
    $scope.company_name = '';
    $scope.selecting_item = false;
    $scope.item_selected = false;
    $scope.purchase = {
        'purchase_items': [],
        'purchase_invoice_number': '',
        'vendor_invoice_number': '',
        'vendor_do_number': '',
        'vendor_invoice_date': '',
        'purchase_invoice_date': '',
        'brand': '',
        'vendor': '',
        'transport': '',
        'discount': 0,
        'net_total': 0,
        'purchase_expense': 0,
        'grant_total': 0,
        'vendor_amount': 0,
        'deleted_items': []
    }
    $scope.purchase.vendor_name = 'select';
    $scope.purchase.brand = 'select';
    $scope.purchase.transport = 'select';
    $scope.item_name = '';
    $scope.item_code = '';
    $scope.barcode = '';
    $scope.init = function(csrf_token, invoice_number)
    {
        $scope.csrf_token = csrf_token;
        $scope.purchase.purchase_invoice_number = invoice_number;
        $scope.popup = '';

        new Picker.Date($$('#vendor_invoice_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        new Picker.Date($$('#purchase_invoice_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });

        $scope.get_vendors();
        $scope.get_brands();
        $scope.get_companies();

    }

    $scope.get_vendors = function() {
        $http.get('/vendor/list/').success(function(data)
        {
            $scope.vendors = data.vendors;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.add_vendor = function() {
        if($scope.purchase.vendor_name == 'other') {
            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '36%',
                'message_padding': '0px',
                'left': '28%',
                'top': '40px',
                'height': 'auto',
                'content_div': '#add_vendor'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
        }
    }

    $scope.add_new_vendor = function() {
        params = { 
            'name':$scope.vendor_name,
            'contact_person': $scope.contact_person,
            'house': $scope.house_name,
            'street': $scope.street,
            'city': $scope.city,
            'district':$scope.district,
            'pin': $scope.pin,
            'mobile': $scope.mobile,
            'phone': $scope.land_line,
            'email': $scope.email_id,
            "csrfmiddlewaretoken" : $scope.csrf_token
        }
        $http({
            method : 'post',
            url : "/register/vendor/",
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data, status) {
            
            if (data.result == 'error'){
                $scope.error_flag=true;
                $scope.message = data.message;
            } else {
                $scope.popup.hide_popup();                             
                $scope.get_vendors();
                $scope.purchase.vendor_name = $scope.vendor_name;
                $scope.purchase.vendor_name = data.vendor_name;
                $scope.vendor_name = '';
                $scope.contact_person = '';
                $scope.house_name = '';
                $scope.street = '';
                $scope.city = '';
                $scope.district = '';
                $scope.pin = '';
                $scope.mobile = '';
                $scope.land_line = '';
                $scope.email_id = '';
            }
        }).error(function(data, success){
            
        });
    }

    $scope.get_brands = function() {
        $http.get('/inventory/brand_list/').success(function(data)
        {
            $scope.brands = data.brands;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.add_brand = function() {
        if($scope.purchase.brand == 'other') {
            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '27%',
                'message_padding': '0px',
                'left': '28%',
                'top': '150px',
                'height': '115px',
                'content_div': '#add_brand'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();

        }
    }

    $scope.add_new_brand = function() {
        params = { 
            'brand_name':$scope.brand_name,
            "csrfmiddlewaretoken" : $scope.csrf_token
        }
        $http({
            method : 'post',
            url : "/inventory/add/brand/",
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data, status) {
            
            if (data.result == 'error'){
                $scope.error_flag=true;
                $scope.message = data.message;
            } else {
                $scope.error_flag=false;
                $scope.message = '';
                $scope.popup.hide_popup();
                $scope.get_brands();
                $scope.purchase.brand = $scope.brand_name;                
            }
        }).error(function(data, success){
            
        });
    }

    $scope.get_companies = function() {
        $http.get('/company_list/').success(function(data)
        {
            $scope.companies = data.company_names;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.add_transport = function() {
        if($scope.purchase.transport == 'other') {
            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '27%',
                'message_padding': '0px',
                'left': '28%',
                'top': '150px',
                'height': '115px',
                'content_div': '#add_company'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
        }
    }

    $scope.add_new_company = function() {
        params = { 
            'new_company':$scope.company_name,
            "csrfmiddlewaretoken" : $scope.csrf_token
        }
        $http({
            method : 'post',
            url : "/add_company/",
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data, status) {
            
            if (data.result == 'error'){
                $scope.error_flag=true;
                $scope.message = data.message;
            } else {
                $scope.popup.hide_popup();
                $scope.get_companies();
                $scope.purchase.transport = $scope.company_name;
                $scope.company_name = '';
                $scope.error_flag=false;
                $scope.message = '';
            }
        }).error(function(data, success){
            
        });
    }

    $scope.getItems = function(parameter){

        $scope.validation_error = '';
        if(parameter == 'item_code')
            var param = $scope.item_code;
        else if(parameter == 'item_name')
            var param = $scope.item_name;
        else if (parameter == 'barcode')
            var param = $scope.barcode;
        if($scope.purchase.brand == 'select'){
            $scope.validation_error = 'Please select brand';
            return false;
        }
        if($scope.item_code == '' && $scope.item_name == '' && $scope.barcode == '') {
            $scope.items = [];
            return false;
        }
        $http.get('/inventory/items/?'+parameter+'='+param+'&brand='+$scope.purchase.brand).success(function(data)
        {
            $scope.selecting_item = true;
            $scope.item_selected = false;
            $scope.items = data.items;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }

    $scope.addPurchaseItem = function(item) {
        $scope.selecting_item = false;
        $scope.item_selected = true;
        $scope.item_code = '';
        $scope.item_name = '';
        $scope.barcode = '';
        $scope.item_select_error = '';
        if($scope.purchase.purchase_items.length > 0) {
            for(var i=0; i< $scope.purchase.purchase_items.length; i++) {
                if($scope.purchase.purchase_items[i].item_code == item.item_code) {
                    $scope.item_select_error = "Item already selected";
                    return false;
                }
            }
        } 
        var selected_item = {
            'item_code': item.item_code,
            'item_name': item.item_name,
            'barcode': item.barcode,
            'uom': item.uom,
            'current_stock': item.current_stock,
            'frieght': 0,
            'frieght_unit': 0,
            'handling': 0,
            'handling_unit': 0,
            'tax': item.tax,
            'selling_price': 0,
            'qty_purchased': 0,
            'cost_price': 0,
            'permit_disc_amt': 0,
            'permit_disc_percent': 0,
            'net_amount': 0,
            'unit_price': 0,
            'expense': 0,
            'expense_unit': 0
        }
        $scope.purchase.purchase_items.push(selected_item);
    }
    $scope.delete_purchase_item = function(item){
        var index = $scope.purchase.purchase_items.indexOf(item);
        $scope.purchase.purchase_items.splice(index, 1);
        $scope.purchase.deleted_items.push(item);
    }
    $scope.calculate_frieght = function(item){
        if(item.frieght != Number(item.frieght)){
            item.frieght = 0;
        }
        if(item.qty_purchased != '' && item.frieght != ''){
            item.frieght_unit = parseFloat(item.frieght)/parseFloat(item.qty_purchased);
        }
        $scope.calculate_net_amount(item);
        $scope.calculate_cost_price(item);
    }
    $scope.calculate_handling = function(item){
        if(item.handling != Number(item.handling)) {
            item.handling = 0;
        }
        if(item.qty_purchased != '' && item.handling != ''){
            item.handling_unit = parseFloat(item.handling)/parseFloat(item.qty_purchased);
        }
        $scope.calculate_cost_price(item);
        $scope.calculate_net_amount(item);
    }
    $scope.calculate_expense = function(item){
        if(item.expense != Number(item.expense)){
            item.expense = 0;
        }
        if(item.qty_purchased != '' && item.expense != ''){
            item.expense_unit = parseFloat(item.expense)/parseFloat(item.qty_purchased);
        }
        $scope.calculate_cost_price(item);
        $scope.calculate_net_amount(item);
        $scope.calculate_purchase_expense();
    }
    $scope.calculate_cost_price = function(item) {
        if(item.unit_price == '' || item.unit_price != Number(item.unit_price)){
            item.unit_price = 0;
        }
        if(item.unit_price != '' || item.frieght_unit != '' || item.handling_unit != '' || item.expense_unit != ''){
            item.cost_price = parseFloat(item.unit_price) + parseFloat(item.frieght_unit) + parseFloat(item.handling_unit) + parseFloat(item.expense_unit)
        }
        $scope.calculate_net_amount(item);
    }

    $scope.calculate_net_amount = function(item) {
        if(item.qty_purchased == '' || item.qty_purchased != Number(item.qty_purchased)) {
            item.qty_purchased = 0;
        }
        if(item.unit_price != Number(item.unit_price)) {
            item.unit_price = 0;
        }
        if(item.qty_purchased != '' && item.unit_price != ''){
            if(item.frieght == '' || item.frieght != Number(item.frieght)){
                item.frieght = 0;
            }
            if(item.handling == '' || item.handling != Number(item.handling)){
                item.handling = 0;
            }
            if(item.expense == '' || item.expense != Number(item.expense)){
                item.expense = 0;
            }            
            
            item.net_amount = ((parseFloat(item.qty_purchased)*parseFloat(item.unit_price)) + parseFloat(item.frieght)+ parseFloat(item.handling)+parseFloat(item.expense)).toFixed(3);
        }
        $scope.calculate_vendor_amount();
        $scope.calculate_net_total();
    }
    $scope.calculate_discount_amt = function(item) {
        if(item.selling_price == '' || item.selling_price != Number(item.selling_price)) {
            item.selling_price = 0;
        }
        if(item.permit_disc_percent == '' || item.permit_disc_percent != Number(item.permit_disc_percent)){
            item.permit_disc_percent = 0;
        }
        if(item.permit_disc_percent == '' || item.permit_disc_percent != Number(item.permit_disc_percent)){
            item.permit_disc_percent = 0;
        }
        if((item.permit_disc_percent != '' || item.permit_disc_percent != 0) && (item.selling_price != '' || item.selling_price != 0)) {
            item.permit_disc_amt = (parseFloat(item.selling_price)*parseFloat(item.permit_disc_percent))/100;
        }
    }

    $scope.calculate_discount_percent = function(item) {
        if(item.selling_price == '' || item.selling_price != Number(item.selling_price)) {
            item.selling_price = 0;
        }
        if(item.permit_disc_percent == '' || item.permit_disc_percent != Number(item.permit_disc_percent)){
            item.permit_disc_percent = 0;
        }
        if(item.permit_disc_percent == '' || item.permit_disc_percent != Number(item.permit_disc_percent)){
            item.permit_disc_percent = 0;
        }
        if((item.permit_disc_amt != '' || item.permit_disc_amt != '') && (item.selling_price != '' || item.selling_price != 0)) {
            item.permit_disc_percent = (parseFloat(item.permit_disc_amt)/parseFloat(item.selling_price))*100;
        }
    }

    $scope.calculate_vendor_amount = function() {
        var vendor_amount = 0;
        for(i=0; i<$scope.purchase.purchase_items.length; i++){
            vendor_amount = vendor_amount + (parseFloat($scope.purchase.purchase_items[i].unit_price)*parseFloat($scope.purchase.purchase_items[i].qty_purchased));
        }

        $scope.purchase.vendor_amount = vendor_amount;
    }

    $scope.calculate_net_total = function(){
        var net_total = 0;
        for(i=0; i<$scope.purchase.purchase_items.length; i++){
            net_total = net_total + parseFloat($scope.purchase.purchase_items[i].net_amount);
        }
        $scope.purchase.net_total = net_total;
        $scope.calculate_grant_total();
    }

    $scope.calculate_purchase_expense = function(){
        var purchase_expense = 0;
        for(i=0; i<$scope.purchase.purchase_items.length; i++){
            purchase_expense = purchase_expense + parseFloat($scope.purchase.purchase_items[i].expense);
        }
        $scope.purchase.purchase_expense = purchase_expense;
    }

    $scope.calculate_grant_total = function(){
        $scope.purchase.grant_total = $scope.purchase.net_total - $scope.purchase.discount;
    }
    $scope.validate_purchase = function() {
        $scope.purchase.purchase_invoice_date = $$('#purchase_invoice_date')[0].get('value');
        $scope.purchase.vendor_invoice_date = $$('#vendor_invoice_date')[0].get('value');
        $scope.validation_error = '';
        if($scope.purchase.vendor_invoice_number == '') {
            $scope.validation_error = "Please Enter Vendor invoice number" ;
            return false;
        } else if($scope.purchase.vendor_do_number == ''){
            $scope.validation_error = "Please enter Vendor D.O number";
            return false;
        } else if($scope.purchase.vendor_invoice_date == '') {
            $scope.validation_error = "Please enter vendor invoice date";
            return false;
        } else if($scope.purchase.purchase_invoice_date == ''){
            $scope.validation_error = "Please enter purchase invoice date";
            return false;
        } else if($scope.purchase.brand == 'select') {
            $scope.validation_error = "Please select brand";            
            return false;
        } else if($scope.purchase.vendor_name == 'select') {
            $scope.validation_error = "Please select vendor";
            return false;
        } else if($scope.purchase.transport == 'select') {
            $scope.validation_error = "Please select Transportation company";
            return false;
        } else if($scope.purchase.purchase_items.length == 0){
            $scope.validation_error = "Please Choose Item";
            return false;
        } else if(!(Number($scope.purchase.purchase_invoice_number) == $scope.purchase.purchase_invoice_number)) {
            
            $scope.validation_error = "Please enter a number as purchase invoice number";
            return false;
        }
        else if(!(Number($scope.purchase.discount) == $scope.purchase.discount)) {
            $scope.validation_error = "Please enter a number as discount";
        }
        else {
            return true;
        }        
    }

    $scope.save_purchase = function() {
        if($scope.validate_purchase()) {
            params = { 
                'purchase': angular.toJson($scope.purchase),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/purchase/entry/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                document.location.href = '/purchase/entry/';
               
            }).error(function(data, success){
                
            });
        }
    }

    $scope.load_purchase = function() {
        $http.get('/purchase/?invoice_no='+$scope.purchase.purchase_invoice_number).success(function(data)
        {
            $scope.selecting_item = true;
            $scope.item_selected = false;
            $scope.purchase = data.purchase;
            $scope.purchase.deleted_items = [];
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }

    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }
}

function SalesQNDNController($scope, $element, $http, $timeout, share, $location) {

    $scope.items = [];
    $scope.selected_item = '';
    $scope.customer = '';
    $scope.staff = '';
    $scope.selecting_item = false;
    $scope.item_selected = false;
    $scope.payment_mode = 'cash';
    $scope.payment_mode_selection = true;
    $scope.payment_mode_selection_check = true;

    $scope.sales = {
        'sales_items': [],
        'sales_invoice_number': '',
        'date_sales': '',
        'customer':'',
        'staff': '',
        'net_total': 0,
        'payment_mode':'cash',
        'card_number':'',
        'bank_name':'',
        'net_discount': 0,
        'roundoff': 0,
        'grant_total': 0,
        'paid': 0,
        'balance': 0,
        'quotation_ref_no':'',
        'delivery_no': '',   
    }
    $scope.sales.staff = 'select';
    $scope.sales.customer = '';
    $scope.init = function(csrf_token, sales_invoice_number)
    {
        $scope.csrf_token = csrf_token;
        $scope.sales.sales_invoice_number = sales_invoice_number;
        $scope.popup = '';
        
        
        $scope.get_staff();
            
    }
    $scope.payment_mode_change_sales = function(payment_mode) {
        if(payment_mode == 'cheque') {
            $scope.payment_mode_selection = true;
            $scope.payment_mode_selection_check = false;
            
            var date_picker = new Picker.Date($$('#sales_invoice_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
            
        }
        else if(payment_mode == 'card'){
            $scope.payment_mode_selection = false;
        }
        else {
            
            $scope.payment_mode_selection = true;
            $scope.payment_mode_selection_check = true;
        }
    }
    $scope.validate_sales = function() {

        if ($scope.sales.quotation_ref_no == ''){
            $scope.validation_error = "Enter Quotation Reference No" ;
            return false;
        } else if($scope.sales.sales_invoice_date == '') {
            $scope.validation_error = "Enter Sales invoice Date" ;
            return false;
        } else if($scope.sales.customer =='select'){
            $scope.validation_error = "Enter Customer Name";
            return false;
        } else if($scope.sales.staff =='select') {
            $scope.validation_error = "Enter Salesman Name";
            return false;
        } else if($scope.sales.sales_items.length == 0){
            $scope.validation_error = "Choose Item";
            return false;
        }
        else if( $scope.sales.payment_mode == 'card' && ($scope.sales.card_number == '' )) {
            
            
            $scope.validation_error = 'Please Enter Card Number';
            return false;
        } else if( $scope.sales.payment_mode == 'card' && ($scope.sales.bank_name == '' )) {
           
            $scope.validation_error = 'Please Enter Bank Name';
            return false; 
        }
        else {
            return true;
        }        
    }

    $scope.get_staff = function() {
        $http.get('/salesman/list/').success(function(data)
        {           

            $scope.staffs = data.salesmen;

        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
        $scope.add_staff = function() {

        if($scope.sales.staff == 'other') {

            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '384px',
                'message_padding': '0px',
                'left': '28%',
                'top': '40px',
                'height': '702px',
                'content_div': '#'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
        }
    }

    $scope.add_new_staff = function() {
        params = { 
            'name':$scope.staff_name,
            'contact_person': $scope.contact_person,
            'house': $scope.house_name,
            'street': $scope.street,
            'city': $scope.city,
            'district':$scope.district,
            'pin': $scope.pin,
            'mobile': $scope.mobile,
            'phone': $scope.land_line,
            'email': $scope.email_id,
            "csrfmiddlewaretoken" : $scope.csrf_token
        }
        $http({
            method : 'post',
            url : "/register/staff/",
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data, status) {
            
            if (data.result == 'error'){
                $scope.error_flag=true;
                $scope.message = data.message;
            } else {
                $scope.popup.hide_popup();
                $scope.get_staff();
                $scope.sales.staff = $scope.staff_name;
                $scope.sales.staff = data.staff_name;
            }
        }).error(function(data, success){
            
        });
    }

    $scope.get_quotation_details = function(){
        get_quotation_details($http, $scope);        
    }
    $scope.add_quotation = function(quotation) {
        $scope.selecting_quotation = false;
        $scope.quotation_selected = true;
        $scope.item_select_error = '';
        $scope.sales.sales_items = []
        $scope.quotation_no = quotation.ref_no; 
        $scope.delivery_no = quotation.delivery_no;
        $scope.sales.quotation_ref_no = $scope.quotation_no;
        $scope.sales.delivery_no = $scope.delivery_no
        $scope.sales.customer = quotation.customer; 
        $scope.sales.net_total = quotation.net_total;
        if(quotation.items.length > 0){
            for(var i=0; i< quotation.items.length; i++){
                var selected_item = {
                    'sl_no': quotation.items[i].sl_no,
                    'item_code': quotation.items[i].item_code,
                    'item_name': quotation.items[i].item_name,
                    'barcode': quotation.items[i].barcode,
                    'item_description': quotation.items[i].item_description,
                    'qty_sold': quotation.items[i].qty_sold,
                    'current_stock': quotation.items[i].current_stock,
                    'uom': quotation.items[i].uom,
                    'unit_price': quotation.items[i].selling_price,
                    'discount_permit': quotation.items[i].discount_permit,
                    'tax': quotation.items[i].tax,
                    'tax_amount': 0,
                    'discount_permit_amount':0,
                    'disc_given': quotation.items[i].discount_given,
                    'unit_cost':0,
                    'net_amount': quotation.items[i].net_amount,
                }
                // $scope.calculate_tax_amount_sale(selected_item);
                // $scope.calculate_discount_amount_sale(selected_item);
                // $scope.calculate_unit_cost_sale(selected_item);
                $scope.sales.sales_items.push(selected_item);
                $scope.calculate_grant_total_sale();
                $scope.calculate_net_discount_sale();
                
            }
        }
    }


    $scope.get_delivery_note_details = function(){

        var delivery_no = $scope.delivery_no;
        $scope.delivery_notes = []
        $http.get('/sales/delivery_note_details/?delivery_no='+delivery_no).success(function(data)
        {
            if(data.delivery_notes.length > 0){
               $scope.selecting_delivery_note = true;
                $scope.delivery_note_selected = false;
                $scope.delivery_notes = data.delivery_notes; 
            } else {
                $scope.dn_message = "There is no delivery note with this number";
            }
            
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.add_delivery_note = function(delivery_note) {
        $scope.selecting_delivery_note = false;
        $scope.delivery_note_selected = true;
        $scope.item_select_error = '';
        $scope.sales.sales_items = []
        $scope.quotation_no = delivery_note.ref_no; 
        $scope.delivery_no = delivery_note.delivery_no;
        $scope.sales.quotation_ref_no = $scope.quotation_no;
        $scope.sales.delivery_no = $scope.delivery_no
        $scope.sales.customer = delivery_note.customer; 
        $scope.sales.net_total = delivery_note.net_total;
        if(delivery_note.items.length > 0){
            for(var i=0; i< delivery_note.items.length; i++){
                var selected_item = {
                    'sl_no': delivery_note.items[i].sl_no,
                    'item_code': delivery_note.items[i].item_code,
                    'item_name': delivery_note.items[i].item_name,
                    'barcode': delivery_note.items[i].barcode,
                    'item_description': delivery_note.items[i].item_description,
                    'qty_sold': delivery_note.items[i].qty_sold,
                    'current_stock': delivery_note.items[i].current_stock,
                    'uom': delivery_note.items[i].uom,
                    'unit_price': delivery_note.items[i].selling_price,
                    'discount_permit': delivery_note.items[i].discount_permit,
                    'tax': delivery_note.items[i].tax,
                    'tax_amount': 0,
                    'discount_permit_amount':0,
                    'disc_given': delivery_note.items[i].discount_given,
                    'unit_cost':0,
                    'net_amount': delivery_note.items[i].net_amount,
                }
                // $scope.calculate_tax_amount_sale(selected_item);
                // $scope.calculate_discount_amount_sale(selected_item);
                // $scope.calculate_unit_cost_sale(selected_item);
                $scope.sales.sales_items.push(selected_item);
                $scope.calculate_grant_total_sale();
                $scope.calculate_net_discount_sale();
                
            }
        }
    }

    $scope.items = [];
    $scope.selected_item = '';
    $scope.selecting_item = false;
    $scope.item_selected = false;
    $scope.sales_items = [];
    
    $scope.getItems = function(parameter){

        console.log('parameter', parameter);
        if(parameter == 'item_code')
            var param = $scope.item_code;
        else if(parameter == 'item_name')
            var param = $scope.item_name;
        else if (parameter == 'barcode')
            var param = $scope.barcode;
        $http.get('/inventory/items/?'+parameter+'='+param).success(function(data)
        {
            $scope.selecting_item = true;
            $scope.item_selected = false;
            $scope.items = data.items;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }

    $scope.addSalesItem = function(item) {
        $scope.selecting_item = false;
        $scope.item_selected = true;
        $scope.item_code = '';
        $scope.item_name = '';
        $scope.barcode = '';

        $scope.item_select_error = '';
        
        if($scope.sales.sales_items.length > 0) {
            for(var i=0; i< $scope.sales.sales_items.length; i++) {
                if($scope.sales.sales_items[i].item_code == item.item_code) {
                    $scope.item_select_error = "Item already selected";
                    return false;
                }
            }
        } 
        var selected_item = {

            'item_code': item.item_code,
            'item_name': item.item_name,
            'barcode': item.barcode,
            'current_stock': item.current_stock,
            'unit_price': item.selling_price,
            'tax': item.tax,
            'tax_amount':0,
            'qty_sold': 0,
            'uom': item.uom,
            'discount_permit': item.discount_permit,
            'discount_permit_amount':0,
            'disc_given': 0,
            'unit_cost':0,
            'net_amount': 0,
        }
        $scope.calculate_tax_amount_sale(selected_item);
        $scope.calculate_discount_amount_sale(selected_item);
        $scope.calculate_unit_cost_sale(selected_item);
       
        $scope.sales.sales_items.push(selected_item);
    }
    
    
    $scope.calculate_net_amount_sale = function(item) {
        if(parseInt(item.qty_sold) > parseInt(item.current_stock)) {
            $scope.validation_error = "Qauntity not in stock";
            return false;
        }
        if(item.qty_sold != '' && item.unit_price != ''){
            item.net_amount = ((parseFloat(item.qty_sold)*parseFloat(item.unit_price))-parseFloat(item.disc_given)).toFixed(2);
            $scope.calculate_net_discount_sale();
        }
        $scope.calculate_net_total_sale();
    }
    // $scope.calculate_tax_amount_sale = function(item) {
    //     if(item.tax != '' && item.unit_price != ''){
    //         item.tax_amount = (parseFloat(item.unit_price)*parseFloat(item.tax))/100;
    //     }
    // }
    // $scope.calculate_discount_amount_sale = function(item) {
    //     if(item.discount_permit != '' && item.unit_price != ''){
    //         item.discount_permit_amount = (parseFloat(item.unit_price)*parseFloat(item.discount_permit))/100;
            
    //     }
    // }
    // $scope.calculate_unit_cost_sale = function(item) {
    //     if(item.unit_price != ''){
    //         item.unit_cost = (parseFloat(item.unit_price)+parseFloat(item.tax_amount)-parseFloat(item.disc_given)).toFixed(2);
            
    //     }
    // }

    $scope.calculate_net_total_sale = function(){
        var net_total = 0;
        for(i=0; i<$scope.sales.sales_items.length; i++){
            net_total = net_total + parseFloat($scope.sales.sales_items[i].net_amount);
        }
        $scope.sales.net_total = net_total;
        $scope.calculate_grant_total_sale();
        
    }
    $scope.calculate_net_discount_sale = function(){
        
        var net_discount = 0;
        for(i=0; i<$scope.sales.sales_items.length; i++){
           
            net_discount = net_discount + parseFloat($scope.sales.sales_items[i].disc_given);

        }
        $scope.sales.net_discount = net_discount;
    }


    $scope.calculate_grant_total_sale = function(){
        $scope.sales.grant_total = $scope.sales.net_total   - $scope.sales.roundoff;
    }
    $scope.calculate_balance_sale = function () {
        $scope.sales.balance = $scope.sales.grant_total - $scope.sales.paid;
    }
    $scope.save_sales = function() {
        if($scope.validate_sales()){
            $scope.sales.sales_invoice_date = $$('#sales_invoice_date')[0].get('value');
            
            params = { 
                'sales': angular.toJson($scope.sales),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/sales/quotaion_deliverynote_sales/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                document.location.href = '/sales/sales_invoice_pdf/'+data.sales_invoice_id+'/';               
            }).error(function(data, success){
                
            });
        }         
    }
}


function SalesController($scope, $element, $http, $timeout, share, $location) {

    $scope.items = [];
    $scope.selected_item = '';
    $scope.customer = '';
    $scope.customer_name = '';
    $scope.staff = '';
    $scope.selecting_item = false;
    $scope.item_selected = false;
    $scope.payment_mode = 'cash';
    $scope.payment_mode_selection = true;
    $scope.sales = {
        'sales_items': [],
        'sales_invoice_number': '',
        'date_sales': '',
        'customer':'',
        'staff': '',
        'net_total': 0,
        'net_discount': 0,
        'roundoff': 0,
        'grant_total': 0,
        'paid': 0,
        'balance': 0,
        
    }
    $scope.sales.staff = 'select';
    $scope.sales.customer = 'select';
    $scope.init = function(csrf_token, sales_invoice_number)
    {
        $scope.csrf_token = csrf_token;
        $scope.sales.sales_invoice_number = sales_invoice_number;
        $scope.popup = '';
        
        
        $scope.get_staff();
        $scope.get_customers();
            
        console.log("$scope.sales.sales_invoice_number ", $scope.sales.sales_invoice_number );
    }
    $scope.payment_mode_change_sales = function(payment_mode) {
        if(payment_mode == 'cheque') {
            $scope.payment_mode_selection = false;
            
            var date_picker = new Picker.Date($$('#sales_invoice_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
            
        } else {
            $scope.payment_mode_selection = true;
        }
    }
    $scope.validate_sales = function() {
        if($scope.sales.sales_invoice_date == '') {
            $scope.validation_error = "Enter Sales invoice Date" ;
            return false;
        } else if($scope.sales.customer =='select'){
            $scope.validation_error = "Enter Customer Name";
            return false;
        } else if($scope.sales.staff =='select') {
            $scope.validation_error = "Enter Salesman Name";
            return false;
        } else if($scope.sales.sales_items.length == 0){
            $scope.validation_error = "Choose Item";
            return false;
        } 
        return true;
    }


    $scope.get_staff = function() {
        $http.get('/salesman/list/').success(function(data)
        {           

            $scope.staffs = data.salesmen;

        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.add_staff = function() {

        if($scope.sales.staff == 'other') {

            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '384px',
                'message_padding': '0px',
                'left': '28%',
                'top': '40px',
                'height': '702px',
                'content_div': '#'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
        }
    }

    $scope.add_new_staff = function() {
        params = { 
            'name':$scope.staff_name,
            'contact_person': $scope.contact_person,
            'house': $scope.house_name,
            'street': $scope.street,
            'city': $scope.city,
            'district':$scope.district,
            'pin': $scope.pin,
            'mobile': $scope.mobile,
            'phone': $scope.land_line,
            'email': $scope.email_id,
            "csrfmiddlewaretoken" : $scope.csrf_token
        }
        $http({
            method : 'post',
            url : "/register/staff/",
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data, status) {
            
            if (data.result == 'error'){
                $scope.error_flag=true;
                $scope.message = data.message;
            } else {
                $scope.popup.hide_popup();
                $scope.get_staff();
                $scope.sales.staff = $scope.staff_name;
                $scope.sales.staff = data.staff_name;
            }
        }).error(function(data, success){
            
        });
    }

    $scope.get_customers = function() {
        $http.get('/customer/list/').success(function(data)
        {   
            
            $scope.customers = data.customers;

        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.add_customer = function() {

        if($scope.sales.customer == 'other') {
            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '36%',
                'message_padding': '0px',
                'left': '28%',
                'top': '40px',
                'height': 'auto',
                'content_div': '#add_customer'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
        }
    }
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }

    $scope.add_new_customer = function() { 
        
       add_new_customer($http, $scope);
    }

    $scope.items = [];
    $scope.selected_item = '';
    $scope.selecting_item = false;
    $scope.item_selected = false;
    $scope.sales_items = [];
    
    $scope.getItems = function(parameter){

        console.log('parameter', parameter);
        if(parameter == 'item_code')
            var param = $scope.item_code;
        else if(parameter == 'item_name')
            var param = $scope.item_name;
        else if (parameter == 'barcode')
            var param = $scope.barcode;
        $http.get('/inventory/items/?'+parameter+'='+param).success(function(data)
        {
            $scope.selecting_item = true;
            $scope.item_selected = false;
            $scope.items = data.items;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }

    $scope.addSalesItem = function(item) {
        $scope.selecting_item = false;
        $scope.item_selected = true;
        $scope.item_code = '';
        $scope.item_name = '';
        $scope.barcode = '';

        $scope.item_select_error = '';
        
        if($scope.sales.sales_items.length > 0) {
            for(var i=0; i< $scope.sales.sales_items.length; i++) {
                if($scope.sales.sales_items[i].item_code == item.item_code) {
                    $scope.item_select_error = "Item already selected";
                    return false;
                }
            }
        } 
        var selected_item = {

            'item_code': item.item_code,
            'item_name': item.item_name,
            'barcode': item.barcode,
            'current_stock': item.current_stock,
            'unit_price': item.selling_price,
            'tax': item.tax,
            'tax_amount':0,
            'qty_sold': 0,
            'uom': item.uom,
            'discount_permit': item.discount_permit,
            'discount_permit_amount':0,
            'disc_given': 0,
            'unit_cost':0,
            'net_amount': 0,

            
        }
        $scope.calculate_tax_amount_sale(selected_item);
        $scope.calculate_discount_amount_sale(selected_item);
        $scope.calculate_unit_cost_sale(selected_item);
       
        $scope.sales.sales_items.push(selected_item);
    }
    
    
    $scope.calculate_net_amount_sale = function(item) {
        if(item.qty_sold != '' && item.unit_price != ''){
            item.net_amount = ((parseFloat(item.qty_sold)*parseFloat(item.unit_price))+(parseFloat(item.tax_amount)*parseFloat(item.qty_sold))-parseFloat(item.disc_given)).toFixed(2);
            $scope.calculate_net_discount_sale();
        }
        $scope.calculate_net_total_sale();
    }
    $scope.calculate_tax_amount_sale = function(item) {
        if(item.tax != '' && item.unit_price != ''){
            item.tax_amount = (parseFloat(item.unit_price)*parseFloat(item.tax))/100;
        }
    }
    $scope.calculate_discount_amount_sale = function(item) {
        if(item.discount_permit != '' && item.unit_price != ''){
            item.discount_permit_amount = (parseFloat(item.unit_price)*parseFloat(item.discount_permit))/100;
            
        }
    }
    $scope.calculate_unit_cost_sale = function(item) {
        if(item.unit_price != ''){
            item.unit_cost = (parseFloat(item.unit_price)+parseFloat(item.tax_amount)-parseFloat(item.disc_given)).toFixed(2);
            
        }
    }

    $scope.calculate_net_total_sale = function(){
        var net_total = 0;
        for(i=0; i<$scope.sales.sales_items.length; i++){
            net_total = net_total + parseFloat($scope.sales.sales_items[i].net_amount);
        }
        $scope.sales.net_total = net_total;
        $scope.calculate_grant_total_sale();
        
    }
    $scope.calculate_net_discount_sale = function(){
        
        var net_discount = 0;
        for(i=0; i<$scope.sales.sales_items.length; i++){
           
            net_discount = net_discount + parseFloat($scope.sales.sales_items[i].disc_given);

        }
        $scope.sales.net_discount = net_discount;
        
    }


    $scope.calculate_grant_total_sale = function(){
        $scope.sales.grant_total = $scope.sales.net_total   - $scope.sales.roundoff;
    }
    $scope.calculate_balance_sale = function () {
        $scope.sales.balance = $scope.sales.grant_total - $scope.sales.paid;
    }
    $scope.save_sales = function() {

        if($scope.validate_sales()){
            $scope.sales.sales_invoice_date = $$('#sales_invoice_date')[0].get('value');
            
            params = { 
                'sales': angular.toJson($scope.sales),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/sales/entry/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                document.location.href = '/sales/sales_invoice_pdf/'+data.sales_invoice_id+'/';                
            }).error(function(data, success){
                
            });
        }   
        
    }

}

function DailyReportController($scope, $element, $http, $timeout, $location){ 

    $scope.init = function(){ 
        $scope.error_flag = false;      
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
    }   

}

function VendorAccountController($scope, $element, $http, $timeout, $location){  
    $scope.actual_total_amount = 0;
    $scope.actual_amount_paid = 0;
    $scope.actual_balance_amount = 0; 
    $scope.cash = true; 
    $scope.init = function(csrf_token) 
    {
        $scope.csrf_token = csrf_token;
        $scope.vendor_account = {
            'payment_mode': 'cash',
            'total_amount': 0,
            'balance_amount': 0,
            'amount_paid': 0,
        }
        $scope.date_picker = new Picker.Date($$('#vendor_account_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format: '%d/%m/%Y',
        });
        $scope.date_picker_cheque = new Picker.Date($$('#cheque_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format: '%d/%m/%Y',
        });
    }
    $scope.select_payment_mode = function(){
        if($scope.vendor_account.payment_mode == 'cheque') {
            $scope.cash = false;
        } else {
            $scope.cash = true;
        }
    }
    $scope.get_vendor_account_details = function(){
        var vendor = $scope.vendor_account.vendor;
        $http.get('/purchase/vendor_account/?vendor='+$scope.vendor_account.vendor).success(function(data, status)
        {
            if (status==200) {             
                $scope.vendor_account = data.vendor_account;
                $scope.actual_total_amount = data.vendor_account.total_amount;
                $scope.actual_amount_paid = data.vendor_account.amount_paid;
                $scope.actual_balance_amount = data.vendor_account.balance_amount;
                $scope.select_payment_mode();               
            }
            
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.validate_vendor_account = function(){
        if($scope.vendor_account.vendor == '') {
            $scope.validation_error = "Please select Vendor";
            return false;
        } else if($scope.vendor_account.amount == ''){
            $scope.validation_error = "Please enter amount";            
            return false;
        } else if($$('#vendor_account_date')[0].get('value') == '') {
            $scope.validation_error = "Please select date";
            return false;
        }
        if(!$scope.vendor_account.narration){
            $scope.vendor_account.narration = "null";
        }
        if($scope.vendor_account.payment_mode == 'cash') {
            if(!$scope.vendor_account.branch_name)
                $scope.vendor_account.branch_name = "null";
            if(!$scope.vendor_account.bank_name)
                $scope.vendor_account.bank_name = "null";
            if(!$scope.vendor_account.cheque_no)
                $scope.vendor_account.cheque_no = "null";
            if(!$scope.vendor_account.cheque_date)
                $scope.vendor_account.cheque_date = "null";
        } else {
            if(!$scope.vendor_account.branch_name){
                $scope.validation_error = "Please enter branch name";
                return false;
            } else if(!$scope.vendor_account.bank_name){
                $scope.validation_error = "Please enter bank name";
                return false;
            }else if(!$scope.vendor_account.cheque_no){
                $scope.validation_error = "Please enter cheque no";
                return false;
            }else if($$('#cheque_date')[0].get('value') == ''){
                $scope.validation_error = "Please enter cheque date";
                return false;
            }
            if($$('#cheque_date')[0].get('value') != '') {
                $scope.vendor_account.cheque_date = $$('#cheque_date')[0].get('value');
            }
        }
        return true;
    }
    $scope.reset_vendor_account = function(){
        $scope.vendor_account.vendor = '';
        
    }
    // $scope.calculate_vendor_account_amounts = function(){
    //     if($scope.actual_total_amount != 0 && $scope.actual_balance_amount != 0) {
    //         var total_amount = $scope.actual_total_amount;
    //         var balance_amount = $scope.actual_balance_amount;
    //         var amount_paid = $scope.actual_amount_paid;
    //         var amount = $scope.vendor_account.amount
    //         $scope.vendor_account.amount_paid = parseInt(amount) + parseInt(amount_paid);
    //         if(parseInt(balance_amount) > parseInt(amount) ) {
    //             $scope.vendor_account.balance_amount = parseInt(balance_amount) - parseInt(amount);
    //         } else {
    //             $scope.vendor_account.balance_amount = 0
    //         } 
    //     }        
    // }
    $scope.save_vendor_account = function(){
        $scope.vendor_account.vendor_account_date = $$('#vendor_account_date')[0].get('value');
        
        if($scope.validate_vendor_account()) {
            params = { 
                'vendor_account': angular.toJson($scope.vendor_account),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : '/purchase/vendor_account/',
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                document.location.href = '/purchase/vendor_accounts/';
               
            }).error(function(data, success){
                
            });
        }
          
    }
}

function PurchaseReportController($scope, $element, $http, $location) {
    $scope.report_name = 'date';   
    $scope.vendor_name = 'select';
    
    $scope.report_date_wise = true;
    $scope.report_vendor_wise = false;    
    
    $scope.init = function(csrf_token,report_type) {
        $scope.report_type = report_type;
        $scope.csrf_token = csrf_token;
        $scope.set_report_type();
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        
        $scope.get_vendors();

    }
    $scope.get_vendors = function() {
        $http.get('/vendor/list/').success(function(data)
        {
            $scope.vendors = data.vendors;
            $scope.vendor_name = 'select';
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.set_report_type = function(){
        if($scope.report_type == 'date'){
            $scope.report_date_wise = true;
            $scope.report_vendor_wise = false;
        } else if($scope.report_type == 'vendor'){
             $scope.report_date_wise = false;
             $scope.report_vendor_wise = true;
        }
    }

    
}

function ExpenseReportController($scope, $http, $element, $timeout, $location){


    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
    }
    
}

function VendorAccountReportController($scope, $element, $http, $location) {
      
    $scope.report_date_wise_flag = true;
    $scope.report_vendor_wise_flag = false;
    
    $scope.init = function(csrf_token,report_type) {
        $scope.report_type = report_type;
        $scope.csrf_token = csrf_token;
        $scope.get_report_type();
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        
        $scope.get_vendors();

    }
    $scope.get_vendors = function() {
        $http.get('/vendor/list/').success(function(data)
        {
            $scope.vendors = data.vendors;
            $scope.vendor_name = 'select';
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }

    $scope.get_report_type = function(){
        if($scope.report_type == 'date') {
            $scope.report_date_wise_flag = true;
            $scope.report_vendor_wise_flag = false;
        } else if ($scope.report_type == 'vendor') {
            $scope.report_date_wise_flag = false;
            $scope.report_vendor_wise_flag = true;
        }
    }
    
}

function PurchaseReturnReportController($scope, $element, $http, $location) {
    
    
    $scope.report_date_wise = true;
    $scope.report_vendor_wise = false;
    $scope.date_total_amount_flag = false;
    $scope.vendor_total_amount_flag = false;
    $scope.error_flag = false;
    
    $scope.init = function(csrf_token,report_type) {

        $scope.report_type = report_type;
        $scope.csrf_token = csrf_token;
        $scope.get_report();
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        
        $scope.get_vendors();

    }
    $scope.get_vendors = function() {
        $http.get('/vendor/list/').success(function(data)
        {
            $scope.vendors = data.vendors;
            $scope.vendor_name = 'select';
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }

    $scope.get_report = function(){
        if($scope.report_type == 'date') {
            $scope.report_date_wise = true;
            $scope.report_vendor_wise = false;
        } else if ($scope.report_type == 'vendor') {
            $scope.report_date_wise = false;
            $scope.report_vendor_wise = true;
        }
    }
   
}

function StockReportController($scope, $element, $http, $timeout, $location) {
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
        $scope.get_stock();
    }
    $scope.get_stock = function(){
        $http.get('/reports/stock_reports/').success(function(data)
        {
            $scope.stocks = data.stocks;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
}


function SalesReportController($scope, $element, $http, $timeout, $location){

    $scope.report_date_wise = true;
    $scope.report_item_wise = false;
    $scope.report_customer_wise = false;
    $scope.report_salesman_wise = false; 
    $scope.error_flag = false;   
    $scope.report_type = 'date';

    $scope.init = function(csrf_token,report_type){ 

        $scope.report_type = report_type;
        $scope.error_flag = false;
        $scope.get_report_type();
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        
        
        $scope.get_customers();
        $scope.get_salesman();
        $scope.get_items();
    }
    $scope.get_report_type =function() {
        if($scope.report_type == 'date'){
            $scope.error_flag = false;
            $scope.report_date_wise = true;
            $scope.report_item_wise = false;
            $scope.report_customer_wise = false;
            $scope.report_salesman_wise = false;            
            
        }
        else if($scope.report_type == 'item'){
            $scope.error_flag = false;
            $scope.report_date_wise = false;
            $scope.report_item_wise = true;
            $scope.report_customer_wise = false;
            $scope.report_salesman_wise = false;            
            
        }
        else if($scope.report_type == 'customer'){
            $scope.error_flag = false;
            $scope.report_date_wise = false;
            $scope.report_item_wise = false;
            $scope.report_customer_wise = true;
            $scope.report_salesman_wise = false;            
                       
        }
        else if($scope.report_type == 'salesman'){
            $scope.error_flag = false;
            $scope.report_date_wise = false;
            $scope.report_item_wise = false;
            $scope.report_customer_wise = false;
            $scope.report_salesman_wise = true;
                       
        }        
    }
    $scope.get_customers = function() {
        $http.get('/customer/list/').success(function(data)
        {
            $scope.customers = data.customers;
            $scope.customer_name = 'select';
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.get_salesman = function() {
        $http.get('/salesman/list/').success(function(data)
        {
            $scope.salesmen = data.salesmen;
            $scope.salesman_name = 'select';
        })
    }
    $scope.get_items = function(){
        $http.get('/inventory/items/').success(function(data)
        {
            $scope.items = data.items;
            $scope.item = 'select';
        })
    }
    
}

function PurchaseReturnController($scope, $element, $http, $timeout, share, $location) {
    $scope.purchase_return = {
        'purchase_return_date': '',
        'invoice_number': '',
        'purchase_items': [],
        'net_return_total': '',

    }
    $scope.init = function(csrf_token, invoice_number) {
        $scope.csrf_token = csrf_token;
        $scope.purchase_return.invoice_number = invoice_number;
        new Picker.Date($$('#purchase_return_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
    }
  
    $scope.load_purchase = function() {
        var invoice = $scope.purchase.purchase_invoice_number;
        $http.get('/purchase/?invoice_no='+$scope.purchase.purchase_invoice_number).success(function(data)
        {
            $scope.selecting_item = true;
            $scope.item_selected = false;
            $scope.purchase = data.purchase;
            $scope.purchase.deleted_items = [];
            $scope.purchase.purchase_invoice_number = invoice;
            $scope.purchase_return.purchase_items = [];
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.addReturnItems = function(item) {
        var ind = $scope.purchase_return.purchase_items.indexOf(item);
        if(ind >= 0){
            $scope.purchase_return.purchase_items.splice(ind, 1);
        } else {
            $scope.purchase_return.purchase_items.push(item);
            var i = $scope.purchase_return.purchase_items.indexOf(item);
        }    
    }
    $scope.calculate_return_amount = function(item){
        $scope.validation_error = '';
        if(parseInt(item.qty_purchased) <= parseInt(item.already_ret_quantity)) {
            $scope.validation_error = "All quantity already returned";
            return false;
        } else if(parseInt(item.qty_purchased) - parseInt(item.already_ret_quantity) < parseInt(item.returned_quantity)) {
            $scope.validation_error = "This quantity cannot be returned";
            return false;
        }
        if(parseInt(item.current_stock) >= parseInt(item.returned_quantity) && parseInt(item.qty_purchased) >= parseInt(item.returned_quantity)) {
           item.returned_amount = parseInt(item.returned_quantity) * parseFloat(item.cost_price);
            $scope.calculate_net_return_amount(); 
        } else {
            if(parseInt(item.current_stock) >= parseInt(item.returned_quantity)) {
                $scope.validation_error = "Item Not in stock";
            }
            if(parseInt(item.qty_purchased) >= parseInt(item.returned_quantity)) {
                $scope.validation_error = "Quantity exceeds purchased quantity";
            }
            return false;
        }
        
    }
    $scope.calculate_net_return_amount = function() {
        var amount = 0;
        for(var i=0;i<$scope.purchase_return.purchase_items.length;i++) {
            amount = amount + $scope.purchase_return.purchase_items[i].returned_amount;
        }
        $scope.purchase_return.net_return_total = amount;
    }
     $scope.save_purchase_return = function() {
        $scope.purchase_return.purchase_invoice_number = $scope.purchase.purchase_invoice_number;
        
        if($$('#purchase_return_date')[0].get('value') == '') {
            $scope.validation_error = "Please select date";
            return false;
        }
        if($scope.purchase_return.purchase_items.length == 0) {
            $scope.validation_error = "Please select items";
            return false;
        }
        if($scope.purchase_return.net_return_total == '') {
            $scope.validation_error = "Please enter return quantity";
            return false;
        }
        for(var i=0; i< $scope.purchase_return.purchase_items.length; i++){
            $scope.purchase_return.purchase_items[i].selected = "selected";
        }
        $scope.purchase_return.purchase_return_date = $$('#purchase_return_date')[0].get('value');
        params = {
            "csrfmiddlewaretoken" : $scope.csrf_token,
            'purchase_return': angular.toJson($scope.purchase_return),
        }
        $http({
            method : 'post',
            url : "/purchase/return/",
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data, status) {
            document.location.href = '/purchase/return/';
           
        }).error(function(data, success){
            
        });
    }
}

function SalesReturnReportController($scope, $element, $http, $timeout, $location){

    

    $scope.init = function(){ 
        $scope.error_flag = false;      
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
    } 


}

function SalesReturnController($scope, $element, $http, $timeout, share, $location) {
    
    $scope.sales_return = {
        'invoice_number': '',
        'sales_return_date': '',
        'net_amount': '',
        'tax_amount':0,
        'sales_items': [],
    }
    $scope.init = function(csrf_token, invoice_number){
        $scope.csrf_token = csrf_token;
        $scope.sales_return.invoice_number = invoice_number;
        new Picker.Date($$('#sales_return_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
    }
    $scope.validate_salesreturn = function() {
            
        if($scope.sales_return.invoice_number == '') {
            
            $scope.validation_error = "Please Choose an invoice number" ;
            return false;
        } else if($$('#sales_return_date')[0].get('value') == '') {
            $scope.validation_error = "Please enter a Date";
            return false;
        } 
        else {
            return true;
        }        
    }
    $scope.getItems = function(parameter) {
        $scope.items = [];
        $scope.selecting_item = true;
        $scope.item_selected = false;
        for(var i=0; i<$scope.sales.sales_items.length; i++){
            if(parameter == 'item_code') {
                if($scope.item_code == ''){
                    $scope.items = [];
                }
                if($scope.sales.sales_items[i].item_code.indexOf($scope.item_code) == 0) {
                    $scope.items.push($scope.sales.sales_items[i]);
                } else {
                    var ind = $scope.items.indexOf($scope.sales.sales_items[i]);
                    if(ind > 0){
                        $scope.items.splice($scope.sales.sales_items[i], 1);
                    }
                }
            }
            if(parameter == 'item_name') {
                if($scope.item_name == ''){
                    $scope.items = [];
                }
                if($scope.sales.sales_items[i].item_name.indexOf($scope.item_name) == 0) {
                    $scope.items.push($scope.sales.sales_items[i]);
                } else {
                    var ind = $scope.items.indexOf($scope.sales.sales_items[i]);
                    if(ind > 0){
                        $scope.items.splice($scope.sales.sales_items[i], 1);
                    }
                }
            }
            if(parameter == 'barcode') {
                if($scope.barcode == ''){
                    $scope.items = [];
                }
                if($scope.sales.sales_items[i].barcode.indexOf($scope.barcode) == 0) {
                    $scope.items.push($scope.sales.sales_items[i]);
                } else {
                    var ind = $scope.items.indexOf($scope.sales.sales_items[i]);
                    if(ind > 0){
                        $scope.items.splice($scope.sales.sales_items[i], 1);
                    }
                }
            }
        }

    }
    $scope.load_sales = function() {
        var invoice = $scope.sales.sales_invoice_number;
        $http.get('/sales/?invoice_no='+$scope.sales.sales_invoice_number).success(function(data)
        {
            $scope.selecting_item = true;
            $scope.item_selected = false;
            if(data.sales) {
                $scope.sales = data.sales;
                $scope.sales.deleted_items = [];
                $scope.sales.sales_invoice_number = invoice;
                $scope.message = ''
            } else {
                $scope.message = data.result;
            }
                
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }

    $scope.addSalesReturnItems = function(item) {
        $scope.calculate_tax_amount_sales_return(item);
        var ind = $scope.sales_return.sales_items.indexOf(item)
        if(ind >= 0){
            $scope.sales_return.sales_items.splice(ind, 1);
        } else {

            $scope.sales_return.sales_items.push(item);
        } 
               
    }
    $scope.calculate_tax_amount_sales_return = function(item) {
        
        
        if(item.tax != '' && item.unit_price != ''){

            item.tax_amount = (parseFloat(item.unit_price)*parseFloat(item.tax))/100;
        }
    }
    $scope.calculate_return_amount = function(item){
        if($scope.check_return(item)) {
            $scope.validation_error = "";
            item.returned_amount = parseFloat(item.returned_quantity) * (parseFloat(item.unit_price) + parseFloat(item.tax_amount) - parseFloat(item.discount_given) ) ;
            $scope.calculate_net_return_amount();
        }
        else{
                item.returned_amount= 0;
        }


    }
    $scope.calculate_net_return_amount = function() {

        var amount = 0;
        for(var i=0;i<$scope.sales_return.sales_items.length;i++) {
            amount = amount + $scope.sales_return.sales_items[i].returned_amount;
        }
        
        $scope.sales_return.net_return_total = amount;
    }
    $scope.check_return = function(item) {

        
        if(parseInt(item.returned_quantity) > parseInt(item.quantity_sold)) {
            $scope.validation_error = "Check Qauntity Entered with invoice";
            return false;
        }
        else{
            return true;
        }
    }
    $scope.save_sales_return = function() {

        if($scope.validate_salesreturn()) {
            $scope.sales_return.sales_return_date = $$('#sales_return_date')[0].get('value');
            $scope.sales_return.sales_invoice_number = $scope.sales.sales_invoice_number;
            for(var i=0; i< $scope.sales_return.sales_items.length; i++){
                $scope.sales_return.sales_items[i].selected = "selected";
            }
            params = {
                "csrfmiddlewaretoken" : $scope.csrf_token,
                'sales_return': angular.toJson($scope.sales_return),
            }
            $http({
                method : 'post',
                url : "/sales/return/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                document.location.href = '/sales/return/';
               
            }).error(function(data, success){
                
            });
        }
    }    
}


function AddItemController($scope, $http, $element, $location, $timeout) {
    
    $scope.brand_value = 'select';
    $scope.brand_name = '';
    $scope.uom_value = 'select';
    $scope.uom_name = '';
    $scope.error_flag = false;
    $scope.is_valid = false;
    $scope.message = '';

    $scope.init = function(csrf_token){

        $scope.csrf_token = csrf_token;
        $scope.get_brands();
        $scope.get_uoms();
    }

    $scope.get_brands = function() {
        $http.get('/inventory/brand_list/').success(function(data)
        {
            $scope.brands = data.brands;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.add_brand = function() {
        if($scope.brand_value == 'other') {
            $scope.error_flag = false;
            $scope.message = '';
            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '27%',
                'message_padding': '0px',
                'left': '28%',
                'top': '150px',
                'height': '115px',
                'content_div': '#add_brand'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();

        }
    }

    $scope.add_new_brand = function() {
        params = { 
            'brand_name':$scope.brand_name,
            "csrfmiddlewaretoken" : $scope.csrf_token
        }
        $http({
            method : 'post',
            url : "/inventory/add/brand/",
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data, status) {
            
            if (data.result == 'error'){
                $scope.error_flag=true;
                $scope.message = data.message;
            } else {
                $scope.popup.hide_popup();
                $scope.get_brands();
                $scope.brand_value = $scope.brand_name;  
                $scope.brand_name = '';            
            }
        }).error(function(data, success){
            
        });
    }

    $scope.get_uoms = function() {
        $http.get('/inventory/uom_list/').success(function(data)
        {
            $scope.uoms = data.uoms;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.add_uom = function() {
        if($scope.uom_value == 'other') {
            $scope.error_flag = false;
            $scope.message = '';
            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '27%',
                'message_padding': '0px',
                'left': '28%',
                'top': '150px',
                'height': '115px',
                'content_div': '#add_uom'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();

        }
    }

    $scope.add_new_uom = function() {
        params = { 
            'uom_name':$scope.uom_name,
            "csrfmiddlewaretoken" : $scope.csrf_token
        }
        $http({
            method : 'post',
            url : "/inventory/add/uom/",
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data, status) {
            
            if (data.result == 'error'){
                $scope.error_flag=true;
                $scope.message = data.message;
            } else {
                $scope.popup.hide_popup();
                $scope.get_uoms();
                $scope.uom_value = $scope.uom_name;    
                $scope.uom_name = '';          
            }
        }).error(function(data, success){
            
        });
    }
    $scope.form_validation = function(){
        if ($scope.item_code == '' || $scope.item_code == undefined) {
            $scope.error_flag=true;
            $scope.message = 'Item code cannot be null';
            return false;
        } else if($scope.item_name == '' || $scope.item_name == undefined) {
            $scope.error_flag=true;
            $scope.message = 'Item name cannot be null';
            return false;
        } else if($scope.uom_value == '' || $scope.uom_value == undefined || $scope.uom_value == 'select' || $scope.uom_value == 'other') {
            $scope.error_flag=true;
            $scope.message = 'Please choose Uom';
            return false;
        } else if($scope.brand_value == '' || $scope.brand_value == undefined || $scope.brand_value == 'select' || $scope.brand_value == 'other') {
            $scope.error_flag=true;
            $scope.message = 'Please choose Brand';
            return false;
        }else if($scope.bar_code == '' || $scope.bar_code == undefined) {
            $scope.error_flag=true;
            $scope.message = 'Barcode cannot be null';
            return false;
        } else if($scope.tax == '' || $scope.tax == undefined) {
            $scope.error_flag=true;
            $scope.message = 'Tax cannot be null';
            return false;
        }
        return true;
    }
    $scope.save_item = function() {
        $scope.is_valid = $scope.form_validation();
        if ($scope.is_valid) {
            $scope.error_flag=false;
            $scope.message = '';
            params = { 
                'name':$scope.item_name,
                'code': $scope.item_code,
                'brand': $scope.brand_value,
                'barcode': $scope.bar_code,
                'tax': $scope.tax,
                'description': $scope.item_description,
                'uom': $scope.uom_value,
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/inventory/add_item/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                
                if (data.result == 'error'){
                    $scope.error_flag=true;
                    $scope.message = data.message;
                } else {
                    $scope.error_flag=false;
                    $scope.message = '';
                    document.location.href = '/inventory/add_item/';
                }
            }).error(function(data, status){
                $scope.error_flag=true;
                $scope.message = data.message;
            });
        }
    }
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }
}

function OpeningStockController($scope, $http, $element, $location, $timeout) {
    $scope.init = function(csrf_token) {
        $scope.scrf_token = csrf_token;
        
    }
    $scope.validate = function(){
        $scope.validation_error = '';
        if($scope.quantity == '' || $scope.quantity == undefined ) {
            $scope.validation_error = "Please enter quantity";
            return false;
        } else if($scope.unit_price == '' || $scope.unit_price == undefined ) {
            $scope.validation_error = "Please enter unit price";
            return false;
        } else if($scope.selling_price == '' || $scope.selling_price == undefined) {
            $scope.validation_error = "Please enter selling price";
            return false;
        } else if($scope.discount_permit_amount == '' || $scope.discount_permit_amount == undefined || $scope.discount_permit_percent == '' || $scope.discount_permit_percent == undefined) {
            $scope.validation_error = "Please enter discount";
            return false;
        } else if( $scope.quantity != Number($scope.quantity)){
            $scope.validation_error = "Please enter digits as quantity ";
            return false;
        } else if( $scope.unit_price != Number($scope.unit_price)){
            $scope.validation_error = "Please enter digits as unit price ";
            return false;
        } else if( $scope.selling_price != Number($scope.selling_price)){
            $scope.validation_error = "Please enter digits as selling price ";
            return false;
        }else if( $scope.discount_permit_amount != '' && $scope.discount_permit_amount != Number($scope.discount_permit_amount)){
            $scope.validation_error = "Please enter digits as discount amount ";
            return false;
        }else if( $scope.discount_permit_percent != '' && $scope.discount_permit_percent != Number($scope.discount_permit_percent)){
            $scope.validation_error = "Please enter digits as discount percent ";
            return false;
        } else {
            document.getElementById("opening_stock_form").submit();
            return true;
        }
    }
}

function StockEditController($scope, $http, $element, $location, $timeout) {
    $scope.init = function(csrf_token, item_code) {
        $scope.scrf_token = csrf_token;
        $http.get('/inventory/edit_stock/?item_code='+item_code).success(function(data)
        {
            $scope.stock = data.stock;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.validate = function() {
        $scope.validation_error = '';
        if($scope.stock.quantity == '' || $scope.stock.quantity == undefined ) {
            $scope.validation_error = "Please enter quantity";
            return false;
        } else if($scope.stock.unit_price == '' || $scope.stock.unit_price == undefined ) {
            $scope.validation_error = "Please enter unit price";
            return false;
        } else if($scope.stock.selling_price == '' || $scope.stock.selling_price == undefined) {
            $scope.validation_error = "Please enter selling price";
            return false;
        } else if($scope.stock.discount_permit_amount == '' || $scope.stock.discount_permit_amount == undefined || $scope.stock.discount_permit_percent == '' || $scope.stock.discount_permit_percent == undefined) {
            console.log($scope.stock.discount_permit_amount, $scope.stock.discount_permit_percent)
            $scope.validation_error = "Please enter discount";
            return false;
        } else if( $scope.stock.quantity != Number($scope.stock.quantity)){
            $scope.validation_error = "Please enter digits as quantity ";
            return false;
        } else if( $scope.stock.unit_price != Number($scope.stock.unit_price)){
            $scope.validation_error = "Please enter digits as unit price ";
            return false;
        } else if( $scope.stock.selling_price != Number($scope.stock.selling_price)){
            $scope.validation_error = "Please enter digits as selling price ";
            return false;
        }else if( $scope.stock.discount_permit_amount != '' && $scope.stock.discount_permit_amount != Number($scope.stock.discount_permit_amount)){
            $scope.validation_error = "Please enter digits as discount amount ";
            return false;
        }else if( $scope.stock.discount_permit_percent != '' && $scope.stock.discount_permit_percent != Number($scope.stock.discount_permit_percent)){
            $scope.validation_error = "Please enter digits as discount percent ";
            return false;
        } else {
            document.getElementById("edit_stock_form").submit();
            return true;
        }
    }
}

function QuotationController($scope, $element, $http, $timeout, share, $location) {

    $scope.items = [];
    $scope.selected_item = '';
    $scope.customer = '';
    $scope.selecting_item = false;
    $scope.item_selected = false;
    $scope.customer_name = '';
    $scope.quotation = {
        'sales_items': [],
        'date': '',
        'customer':'',
        'net_total': 0,
        'reference_no': '',
        'attention': '',
        'subject': '',
        'total_amount': '',
        
    }
    $scope.quotation.customer = 'select';
    $scope.init = function(csrf_token, sales_invoice_number)
    {
        $scope.csrf_token = csrf_token;
        $scope.popup = '';        
        $scope.get_customers();            
    }

    $scope.get_customers = function() {
        $http.get('/customer/list/').success(function(data)
        {   

            $scope.customers = data.customers;

        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }

    $scope.add_customer = function() {

        if($scope.quotation.customer == 'other') {

            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '36%',
                'message_padding': '0px',
                'left': '28%',
                'top': '40px',
                'height': 'auto',
                'content_div': '#add_customer'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
        }
    }

    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }

    $scope.add_new_customer = function() { 
        add_new_customer($http, $scope);
        $scope.quotation.customer = $scope.customer_name;      
    }

    $scope.items = [];
    $scope.selected_item = '';
    $scope.selecting_item = false;
    $scope.item_selected = false;
    $scope.sales_items = [];
    
    $scope.getItems = function(parameter){

        if(parameter == 'item_code')
            var param = $scope.item_code;
        else if(parameter == 'item_name')
            var param = $scope.item_name;
        else if (parameter == 'barcode')
            var param = $scope.barcode;
        $http.get('/inventory/items/?'+parameter+'='+param).success(function(data)
        {
            $scope.selecting_item = true;
            $scope.item_selected = false;
            $scope.items = data.items;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }

    $scope.addSalesItem = function(item) {
        $scope.selecting_item = false;
        $scope.item_selected = true;
        $scope.item_code = '';
        $scope.item_name = '';
        $scope.barcode = '';

        $scope.item_select_error = '';
        
        if($scope.quotation.sales_items.length > 0) {
            for(var i=0; i< $scope.quotation.sales_items.length; i++) {
                if($scope.quotation.sales_items[i].item_code == item.item_code) {
                    $scope.item_select_error = "Item already selected";
                    return false;
                }
            }
        } 
        var selected_item = {
            'sl_no': item.sl_no,
            'item_code': item.item_code,
            'item_name': item.item_name,
            'barcode': item.barcode,
            'current_stock': item.current_stock,
            'unit_price': item.selling_price,
            'tax': item.tax,
            'tax_amount':0,
            'qty_sold': 0,
            'uom': item.uom,
            'discount_permit': item.discount_permit,
            'discount_permit_amount':0,
            'disc_given': 0,
            'unit_cost':0,
            'net_amount': 0,    
        }
       
        $scope.quotation.sales_items.push(selected_item);
    }
    
    
    $scope.calculate_net_amount_sale = function(item) {
        $scope.validation_error = "";
        if(parseInt(item.qty_sold) > parseInt(item.current_stock)) {
            $scope.validation_error = "Qauntity not in stock";
            return false;
        } else {
            if(item.qty_sold != '' && item.unit_price != ''){
                item.net_amount = ((parseFloat(item.qty_sold)*parseFloat(item.unit_price))).toFixed(2);
            }
            $scope.calculate_net_total_amount();
        }
    }

    $scope.calculate_net_total_amount = function() {
        var total_amount = 0
        for(var i=0; i< $scope.quotation.sales_items.length; i++){
            total_amount = (parseFloat(total_amount) + parseFloat($scope.quotation.sales_items[i].net_amount)).toFixed(2);
        }
        $scope.quotation.total_amount = total_amount;
        console.log($scope.quotation.total_amount);
    }

    $scope.quotation_validation = function(){

        $scope.quotation.date = $$('#quotation_date')[0].get('value');
        $scope.quotation.reference_no = $$('#reference_number')[0].get('value');

        if ($scope.quotation.date == '' || $scope.quotation.date == undefined) {
            $scope.validation_error = "Enter quotation Date" ;
            return false;
        } else if ($scope.quotation.customer == 'select') {
            $scope.validation_error = "Enter Customer Name";
            return false;
        } else if ($scope.quotation.reference_no == '' || $scope.quotation.reference_no == undefined) {
            $scope.validation_error = "Enter Reference number";
            return false;
        } else if ($scope.quotation.attention == '' || $scope.quotation.attention == undefined) {
            $scope.validation_error = "Enter attention";
            return false;
        } else if ($scope.quotation.subject == '' || $scope.quotation.subject == undefined) {
            $scope.validation_error = "Enter subject";
            return false;
        } else if($scope.quotation.sales_items.length == 0){
            $scope.validation_error = "Choose Item";
            return false;
        } 
        return true;
    }
    $scope.create_quotation = function() {
        $scope.is_valid = $scope.quotation_validation();
        if($scope.is_valid) {
            params = { 
                'quotation': angular.toJson($scope.quotation),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/sales/create_quotation/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                
                if (data.result == 'error'){
                    $scope.error_flag=true;
                    $scope.message = data.message;
                } else {
                    // console.log('created')
                    document.location.href = '/sales/create_quotation_pdf/'+data.quotation_id+'/';

                }
            }).error(function(data, success){
                
            });
        }
    }

}

function DeliveryNoteController($scope, $element, $http, $timeout, share, $location) {

    $scope.quotation = {
        'sales_items': [],
        'customer':'',
        'reference_no': '',
        'net_total': '',
    }
    $scope.delivery_note = {
        'date':'',
        'lpo_no': '',
        'delivery_note_no': '',
        'quotation_no': ''
    }
    $scope.quotation.customer = '';
    $scope.quotation_no = ''
    $scope.init = function(csrf_token, sales_invoice_number)
    {
        $scope.csrf_token = csrf_token;
        $scope.popup = '';    
    }

    $scope.quotations = [];
    $scope.selected_item = '';
    $scope.selecting_quotation = false;
    $scope.quotation_selected = false;

    $scope.get_quotation_details = function(){
        get_quotation_details($http, $scope);
    }
    $scope.add_quotation = function(quotation) {
        $scope.selecting_quotation = false;
        $scope.quotation_selected = true;
        $scope.item_select_error = '';
        $scope.quotation.sales_items = []
        $scope.quotation_no = quotation.ref_no; 
        $scope.quotation.customer = quotation.customer; 
        console.log(quotation);
        console.log($scope.quotation);
        $scope.quotation.net_total = quotation.net_total;

        if(quotation.items.length > 0){
            for(var i=0; i< quotation.items.length; i++){
                var selected_item = {
                    'sl_no': quotation.items[i].sl_no,
                    'item_code': quotation.items[i].item_code,
                    'item_name': quotation.items[i].item_name,
                    'barcode': quotation.items[i].barcode,
                    'item_description': quotation.items[i].item_description,
                    'qty_sold': quotation.items[i].qty_sold,
                    'disc_given': quotation.items[i].discount_given,
                    'net_amount': quotation.items[i].net_amount,
                    'unit_price': quotation.items[i].selling_price,
                    'current_stock': quotation.items[i].current_stock,
                }
                $scope.quotation.sales_items.push(selected_item);
            }
        }
    }
    $scope.calculate_net_amount_sale = function(item) {
        if(parseInt(item.qty_sold) > parseInt(item.current_stock)) {
            $scope.validation_error = "Qauntity not in stock";
            return false;
        }
        if(item.qty_sold != '' && item.unit_price != ''){
            item.net_amount = ((parseFloat(item.qty_sold)*parseFloat(item.unit_price))-parseFloat(item.disc_given)).toFixed(2);
            $scope.calculate_net_discount_sale();
        }
        $scope.calculate_net_total_sale();
    }
    $scope.calculate_net_total_sale = function(){
        var net_total = 0;
        for(i=0; i<$scope.quotation.sales_items.length; i++){
            net_total = net_total + parseFloat($scope.quotation.sales_items[i].net_amount);
        }
        $scope.quotation.net_total = net_total;
        
    }
    $scope.delivery_note_validation = function(){

        $scope.delivery_note.date = $$('#delivery_note_date')[0].get('value');
        $scope.delivery_note.delivery_note_no = $$('#delivery_no')[0].get('value');
        $scope.delivery_note.lpo_no = $$('#lpo_no')[0].get('value');
        $scope.delivery_note.quotation_no = $scope.quotation_no;

        if ($scope.delivery_note.date == '' || $scope.delivery_note.date == undefined) {
            $scope.validation_error = "Enter Date" ;
            return false;
        } else if ($scope.delivery_note.delivery_note_no == '') {
            $scope.validation_error = "Enter Delivery Note No";
            return false;
        } else if ($scope.delivery_note.quotation_no == '') {
            $scope.validation_error = "Enter Quotation Reference No";
            return false;
        } 
        return true;
    }
    $scope.create_delivery_note = function() {
        $scope.is_valid = $scope.delivery_note_validation();
        if($scope.is_valid) {
            console.log($scope.quotation);
            params = { 
                'quotation': angular.toJson($scope.quotation), 
                'delivery_note': angular.toJson($scope.delivery_note),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/sales/create_delivery_note/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                
                if (data.result == 'error'){
                    $scope.error_flag=true;
                    $scope.message = data.message;
                } else {
                    document.location.href = '/sales/delivery_note_pdf/'+data.delivery_note_id+'/';
                }
            }).error(function(data, success){
                
            });
        }
    }

}



