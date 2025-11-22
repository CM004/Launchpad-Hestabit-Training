"use client"; 
import { Line } from "react-chartjs-2";
import {Chart as ChartJS,CategoryScale,LinearScale,PointElement,LineElement,Filler,Tooltip,Legend,} from "chart.js";
ChartJS.register(CategoryScale,LinearScale,PointElement,LineElement,Filler,Tooltip,Legend);

export default function AreaChart() {
  const data = {
    labels: ["Mar 1", "Mar 3", "Mar 5", "Mar 7", "Mar 9", "Mar 11", "Mar 13"],
    datasets: [
      {
        label: "Revenue",
        data: [10000, 35000, 25000,24000, 27000,25000, 32000, 35000,40000],
        fill: true,
        borderColor: "indigo",
        backgroundColor: "rgba(249, 222, 253, 0.3)",
        tension: 0.7,
        beginAtZero: true,
      },
    ],
  };

//   const options = {
//     plugins: {
//       legend: { display: false },
//     },
//     scales: {
//       y: {
//         beginAtZero: true,
//       },
//     },
//   };

  return <Line data={data} className="p-4" />;
}