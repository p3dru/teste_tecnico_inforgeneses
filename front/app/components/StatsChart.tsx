'use client';

import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend,
    CategoryScale,
    LinearScale,
    BarElement,
    Title
} from 'chart.js';
import { Doughnut, Bar } from 'react-chartjs-2';
import { Report } from '@/lib/api';

ChartJS.register(
    ArcElement,
    Tooltip,
    Legend,
    CategoryScale,
    LinearScale,
    BarElement,
    Title
);

interface StatsChartProps {
    reports: Report[];
}

export default function StatsChart({ reports }: StatsChartProps) {
    // 1. Calculate Status Counts
    const statusCounts = {
        DONE: 0,
        PROCESSING: 0,
        ERROR: 0
    };

    reports.forEach(r => {
        if (r.status in statusCounts) {
            statusCounts[r.status as keyof typeof statusCounts]++;
        }
    });

    // 2. Data for Doughnut (Status)
    const doughnutData = {
        labels: ['Done', 'Processing', 'Error'],
        datasets: [
            {
                data: [statusCounts.DONE, statusCounts.PROCESSING, statusCounts.ERROR],
                backgroundColor: [
                    'rgba(74, 222, 128, 0.6)', // Green
                    'rgba(250, 204, 21, 0.6)', // Yellow
                    'rgba(248, 113, 113, 0.6)', // Red
                ],
                borderColor: [
                    'rgba(74, 222, 128, 1)',
                    'rgba(250, 204, 21, 1)',
                    'rgba(248, 113, 113, 1)',
                ],
                borderWidth: 1,
            },
        ],
    };

    // 3. Reports per Day (Simple Bar Chart)
    const reportsPerDay: Record<string, number> = {};
    reports.forEach(r => {
        const date = new Date(r.created_at).toLocaleDateString();
        reportsPerDay[date] = (reportsPerDay[date] || 0) + 1;
    });

    const sortedDates = Object.keys(reportsPerDay).sort((a, b) => new Date(a).getTime() - new Date(b).getTime()).slice(-7); // Last 7 days

    const barData = {
        labels: sortedDates,
        datasets: [
            {
                label: 'Reports per Day',
                data: sortedDates.map(d => reportsPerDay[d]),
                backgroundColor: 'rgba(249, 115, 22, 0.5)', // Orange
                borderColor: 'rgba(249, 115, 22, 1)',
                borderWidth: 1,
            },
        ],
    };

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div className="bg-white p-6 rounded-2xl shadow-lg border border-gray-100">
                <h3 className="text-gray-700 font-semibold mb-4 text-center">Execution Status</h3>
                <div className="h-64 flex justify-center">
                    <Doughnut data={doughnutData} options={{ maintainAspectRatio: false }} />
                </div>
            </div>

            <div className="bg-white p-6 rounded-2xl shadow-lg border border-gray-100">
                <h3 className="text-gray-700 font-semibold mb-4 text-center">Activity (Last 7 Days)</h3>
                <div className="h-64">
                    <Bar
                        data={barData}
                        options={{
                            maintainAspectRatio: false,
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    ticks: { stepSize: 1 }
                                }
                            }
                        }}
                    />
                </div>
            </div>
        </div>
    );
}
