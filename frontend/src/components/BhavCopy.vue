<template>
    <div class="bhavcopy" id="bhavcopy">
        <div class="container pt-4 pb-4 pl-4 pr-4">
            <div class="is-text-center mb-6">
                <form class="my-form" action="" method="post">
                    <label for="search">Search:</label>
                    <input class="input" type="text" name="search" placeholder="Enter Name" v-model="search">
                    <button class="button is-info" type="submit" v-on:click="searchBhavcopy">Submit</button>
                </form>
            </div>
            <div class="table-container">
                <table class="table is-striped is-hoverable is-fullwidth" id="resultTable">
                    <thead>
                        <tr>
                        <th><abbr title="Position">Pos</abbr></th>
                        <th>Code</th>
                        <th>Name</th>
                        <th>Open</th>
                        <th>High</th>
                        <th>Low</th>
                        <th>Close</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(item, index) in result" :key="index">
                            <td>{{ index }}</td>
                            <td>{{ item.code }}</td>
                            <td>{{ item.name }}</td>
                            <td>{{ item.open }}</td>
                            <td>{{ item.high }}</td>
                            <td>{{ item.low }}</td>
                            <td>{{ item.close }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <button class="button is-info" v-on:click="saveAsCSV">Download Report</button>
            <p>*Report will be available in CSV format.</p>
        </div>
    </div>
</template>

<script>
const axios = require("axios")
export default {
  name: 'BhavCopy',
  props: {
  },
  data() {
      return {
          count: null,
          result: null
      }
  },
  mounted(){
      axios
        .get('http://localhost:8000/api/v1/bhavcopy/')
        .then(response => {
            this.count = response.data.count,
            this.result = response.data.items
        })
  },
  methods: {
        searchBhavcopy(){
            event.preventDefault();
            let query = this.search
            console.log(query)
            axios
            .get('http://localhost:8000/api/v1/bhavcopy/' + this.search)
            .then(response => {
                this.count = response.data.count;
                this.result = response.data.items
            })


        },
        saveAsCSV(){
            event.preventDefault();

            // Select rows from table_id
            var table_id = 'resultTable';
            var separator = ',';
            var rows = document.querySelectorAll('table#' + table_id + ' tr');
            // Construct csv
            var csv = [];
            for (var i = 0; i < rows.length; i++) {
                var row = [], cols = rows[i].querySelectorAll('td, th');
                for (var j = 0; j < cols.length; j++) {
                    // Clean innertext to remove multiple spaces and jumpline (break csv)
                    var data = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/(\s\s)/gm, ' ')
                    data = data.replace(/"/g, '""');
                    // Push escaped string
                    row.push('"' + data + '"');
                }
                csv.push(row.join(separator));
            }
            var csv_string = csv.join('\n');
            // Download it
            var filename = 'export_' + 'bhavcopy' + '_' + new Date().toLocaleDateString() + '.csv';
            var link = document.createElement('a');
            link.style.display = 'none';
            link.setAttribute('target', '_blank');
            link.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv_string));
            link.setAttribute('download', filename);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
  },
}
</script>

<style>
    .my-form{
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .my-form label,
    .my-form input{
        margin-right: 20px
    }
    .my-form input {
        max-width: 150px;
    }
</style>