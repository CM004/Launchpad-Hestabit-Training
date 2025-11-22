"use client";
import { Bar } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip, plugins } from "chart.js";
ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip);

export default function BarChart() {
  const data = {
    labels: ["January", "February", "March", "April", "May", "June"],
    datasets: [
      {
        data: [4500, 5000, 6000, 7500, 9000, 15000], 
        backgroundColor: "brown",
        label: "Employee Performance",
      },
    ],
  };

//   const options = {
//     plugins: {
//       legend: {
//         display: false
//       },
//     },
//   };

  return <Bar className='p-4' data={data}/>;
}