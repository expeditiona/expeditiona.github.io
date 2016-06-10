var $TABLE = $('#table');
var $BTN = $('#export-btn');
var $EXPORT = $('#export');

// appends clone row to end of table when plus sign is clicked
$('.table-add').click(function () {
  var $clone = $TABLE.find('tr.hide').clone(true).removeClass('hide table-line');
  $TABLE.find('table').append($clone);
});

// removes row when x is clicked
$('.table-remove').click(function () {
  $(this).parents('tr').detach();
});

// moves row up when up arrow is clicked
$('.table-up').click(function () {
  var $row = $(this).parents('tr');
  if ($row.index() === 1) return; // Don't go above the header
  $row.prev().before($row.get(0));
});

// moves row up when down arrow is clicked
$('.table-down').click(function () {
  var $row = $(this).parents('tr');
  $row.next().after($row.get(0));
});

// A few jQuery helpers for exporting only
jQuery.fn.pop = [].pop;
jQuery.fn.shift = [].shift;

$BTN.click(function () {
  var $rows = $TABLE.find('tr:not(:hidden)');
  var headers = [];
  var data = [];
  
  // Get the headers (add special header logic here)
  $($rows.shift()).find('th:not(:empty)').each(function () {
    headers.push($(this).text().toLowerCase());
  });
  
  // Turn all existing rows into a loopable array
  $rows.each(function () {
    var $td = $(this).find('td');
    var h = {};
    
    // Use the headers from earlier to name our hash keys
    headers.forEach(function (header, i) {
      h[header] = $td.eq(i).text();   
    });
    
    data.push(h);
  });
  
  // Output the result
  $EXPORT.text(JSON.stringify(data));
});



//Show modal
$(window).load(function(){
    $('#myModal').modal('show');
});

$('#help').click(function(){
    $('#myModal').modal('show');
});

$('#contact').click(function(){
    $('#myModalContact').modal('show');
});

$('#allergenModal').click(function(){
    $('#myAllergenModal').modal('show');
});