let quotes = {
  initQuotesWidget: function (wsUri, subsQuotes, is_debug) {
    let ws = new WebSocket(wsUri);
    if (is_debug) {
      ws.onopen = function (event) {
        console.log("connected");
      };
      ws.onclose = function (event) {
        console.log("disconnected");
      };
      ws.onerror = function (event) {
        console.log(event.data);
      };
    }
    ws.onmessage = function (event) {
      let quote = JSON.parse(event.data);
      let row = document.getElementById(quote.symbol.toLowerCase());
      if (row) {
        let old_bid = parseFloat(row.cells[1].innerText);
        let old_ask = parseFloat(row.cells[2].innerText);

        let new_bid = parseFloat(quote.bid);
        let new_ask = parseFloat(quote.ask);

        let ask_td = "";
        let bid_td = "";

        if (old_bid < new_bid) {
          bid_td = '<span class="text-success"><i class="fa fa-long-arrow-up" style="width: 16px"></i>' + quote.bid + '</span>';
        } else if (old_bid > new_bid) {
          bid_td = '<span class="text-warning"><i class="fa fa-long-arrow-down" style="width: 16px"></i>' + quote.bid + '</span>';
        } else if (old_bid === new_bid) {
          bid_td = '<span class="text-primary"><i class="fa fa-ellipsis-h" style="width: 16px"></i>' + quote.bid + '</span>';
        }

        if (old_ask < new_ask) {
          ask_td = '<span class="text-success"><i class="fa fa-long-arrow-up" style="width: 16px"></i>' + quote.ask + '</span>';
        } else if (old_ask > new_ask) {
          ask_td = '<span class="text-warning"><i class="fa fa-long-arrow-down" style="width: 16px"></i>' + quote.ask + '</span>';
        } else if (old_ask === new_ask) {
          ask_td = '<span class="text-primary"><i class="fa fa-ellipsis-h" style="width: 16px"></i>' + quote.ask + '</span>';
        }

        row.cells[1].innerHTML = bid_td;
        row.cells[2].innerHTML = ask_td;

      } else {
        let row = document.createElement('tr');
        row.setAttribute("id", quote.symbol.toLowerCase());

        let col_symbol = document.createElement('td');
        let col_bid = document.createElement('td');
        let col_ask = document.createElement('td');

        let col_symbol_text = document.createTextNode(quote.symbol);

        col_symbol.appendChild(col_symbol_text);
        col_bid.innerHTML = '<span class="text-primary"><i class="fa fa-ellipsis-h" style="width: 16px"></i>' + quote.bid + '</span>';
        col_ask.innerHTML = '<span class="text-primary"><i class="fa fa-ellipsis-h" style="width: 16px"></i>' + quote.ask + '</span>';

        row.appendChild(col_symbol);
        row.appendChild(col_bid);
        row.appendChild(col_ask);

        for (const [qType, qSymbols] of Object.entries(subsQuotes)) {
          if (qSymbols.includes(quote.symbol)) {
            let table = document.getElementById(qType);
            table.appendChild(row);
          }
        }
      }
    };
    return ws;
  }
};