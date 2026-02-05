'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { apiClient, ReportDetail, BoundingBox } from '@/lib/api';

export default function ReportDetailPage() {
    const params = useParams();
    const router = useRouter();
    const [report, setReport] = useState<ReportDetail | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [imgDimensions, setImgDimensions] = useState<{ w: number, h: number } | null>(null);

    useEffect(() => {
        const fetchReport = async () => {
            try {
                if (!params.id) return;
                const data = await apiClient.getReport(params.id as string);
                setReport(data);
            } catch (err) {
                setError('Failed to load report');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        if (apiClient.isAuthenticated()) {
            fetchReport();
        } else {
            router.push('/');
        }
    }, [params.id, router]);

    const handleImageLoad = (e: React.SyntheticEvent<HTMLImageElement>) => {
        const { naturalWidth, naturalHeight } = e.currentTarget;
        setImgDimensions({ w: naturalWidth, h: naturalHeight });
    };

    if (loading) return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
        </div>
    );

    if (error || !report) return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 text-red-500">
            {error || 'Report not found'}
        </div>
    );

    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const imageUrl = `${API_URL}/static/uploads/${report.file_path}`;

    return (
        <div className="min-h-screen bg-gray-50 p-6">
            <div className="max-w-6xl mx-auto">
                <button
                    onClick={() => router.back()}
                    className="mb-6 px-4 py-2 text-gray-600 hover:bg-gray-200 rounded-lg transition-colors flex items-center gap-2"
                >
                    ← Back to Dashboard
                </button>

                <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
                    <div className="p-6 border-b border-gray-100 flex justify-between items-center">
                        <div>
                            <h1 className="text-2xl font-bold text-gray-900">Analysis Result</h1>
                            <p className="text-gray-500 text-sm mt-1">ID: {report.id}</p>
                        </div>
                        <div className={`px-4 py-2 rounded-full font-bold ${report.status === 'DONE' ? 'bg-green-100 text-green-700' :
                                report.status === 'ERROR' ? 'bg-red-100 text-red-700' :
                                    'bg-yellow-100 text-yellow-700'
                            }`}>
                            {report.status}
                        </div>
                    </div>

                    <div className="p-6 grid grid-cols-1 lg:grid-cols-3 gap-8">
                        {/* Image Viewer */}
                        <div className="lg:col-span-2 relative bg-gray-900 rounded-xl overflow-hidden min-h-[400px] flex items-center justify-center">
                            <div className="relative inline-block">
                                <img
                                    src={imageUrl}
                                    alt="Analysis"
                                    className="max-w-full h-auto block"
                                    onLoad={handleImageLoad}
                                />
                                {imgDimensions && report.detections.map((box, idx) => (
                                    <div
                                        key={idx}
                                        className="absolute border-2 border-red-500 bg-red-500/20 hover:bg-red-500/30 transition-colors"
                                        style={{
                                            left: `${(box.x1 / imgDimensions.w) * 100}%`,
                                            top: `${(box.y1 / imgDimensions.h) * 100}%`,
                                            width: `${((box.x2 - box.x1) / imgDimensions.w) * 100}%`,
                                            height: `${((box.y2 - box.y1) / imgDimensions.h) * 100}%`,
                                        }}
                                    >
                                        <span className="absolute -top-7 left-0 bg-red-600 text-white text-xs px-2 py-1 rounded shadow-sm whitespace-nowrap">
                                            {box.class_name} ({Math.round(box.confidence * 100)}%)
                                        </span>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Sidebar Details */}
                        <div className="space-y-6">
                            <div className="bg-gray-50 rounded-xl p-6 border border-gray-200">
                                <h3 className="font-semibold text-gray-900 mb-4">Detection Summary</h3>
                                <div className="space-y-3">
                                    <div className="flex justify-between">
                                        <span className="text-gray-600">Detections Found</span>
                                        <span className="font-medium">{report.detections.length}</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-gray-600">Model Version</span>
                                        <span className="font-medium">{report.model_version || 'N/A'}</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-gray-600">Processing Time</span>
                                        <span className="font-medium">{report.processing_time_ms ? `${report.processing_time_ms.toFixed(2)}ms` : 'N/A'}</span>
                                    </div>
                                </div>
                            </div>

                            <div className="bg-gray-50 rounded-xl p-6 border border-gray-200">
                                <h3 className="font-semibold text-gray-900 mb-4">Objects List</h3>
                                {report.detections.length > 0 ? (
                                    <div className="space-y-2 max-h-[300px] overflow-y-auto pr-2">
                                        {report.detections.map((box, idx) => (
                                            <div key={idx} className="flex justify-between items-center p-2 bg-white rounded border border-gray-200 text-sm">
                                                <span className="font-medium text-gray-800">{box.class_name}</span>
                                                <span className="text-gray-500">{(box.confidence * 100).toFixed(1)}%</span>
                                            </div>
                                        ))}
                                    </div>
                                ) : (
                                    <div className="text-gray-400 italic text-sm">No objects detected</div>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
