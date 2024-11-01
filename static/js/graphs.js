// Fetch User Count by Visibility
fetch('/report/user_count_by_visibility')
.then(response => response.json())
.then(data => {
    const width = 600;
    const height = 400;
    const svg = d3.select("#visibilityGraph")
        .attr("width", width)
        .attr("height", height);

    const x = d3.scaleBand()
        .domain(data.map(d => d.Visibility))
        .range([0, width])
        .padding(0.1);

    const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.user_count)])
        .nice()
        .range([height, 0]);

    // Draw bars
    svg.selectAll(".bar")
        .data(data)
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", d => x(d.Visibility))
        .attr("y", d => y(d.user_count))
        .attr("width", x.bandwidth())
        .attr("height", d => height - y(d.user_count))
        .attr("fill", "steelblue");

    // Add X Axis
    svg.append("g")
        .attr("transform", `translate(0, ${height})`)
        .call(d3.axisBottom(x));

    // Add Y Axis
    svg.append("g")
        .call(d3.axisLeft(y));

})
.catch(error => console.error('Error fetching data:', error));

// Fetch Total Users Graph
fetch('/report/total_users')
.then(response => response.json())
.then(data => {
    const svg = d3.select("#totalUsersGraph")
        .attr("width", width)
        .attr("height", height);

    svg.append("text")
        .attr("x", width / 2)
        .attr("y", height / 2)
        .attr("text-anchor", "middle")
        .text(`Total Users: ${data.total_users}`);
})
.catch(error => console.error('Error fetching total users:', error));

// Fetch Average Visibility Entries Graph
fetch('/report/avg_visibility_entries')
.then(response => response.json())
.then(data => {
    const svg = d3.select("#avgVisibilityGraph")
        .attr("width", width)
        .attr("height", height);

    svg.append("text")
        .attr("x", width / 2)
        .attr("y", height / 2)
        .attr("text-anchor", "middle")
        .text(`Average Public Entries: ${data.avg_public_entries.toFixed(2)}`);
})
.catch(error => console.error('Error fetching average visibility entries:', error));