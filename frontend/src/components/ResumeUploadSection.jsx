import React, { useState } from 'react';
import { UploadCloud, ArrowRight } from 'lucide-react';

export default function ResumeUploadSection({ uploadedResumes, setUploadedResumes, onProceed }) {
  const [uploading, setUploading] = useState(false);

  const handleFileUpload = async (e) => {
    const files = Array.from(e.target.files);
    if (!files.length) return;
    setUploading(true);
    const fd = new FormData();
    files.forEach(f => fd.append('files', f));

    try {
      const res = await fetch('/api/resumes/upload-batch', { method: 'POST', body: fd });
      const data = await res.json();
      if (data.resumes) setUploadedResumes(prev => [...prev, ...data.resumes]);
    } catch (err) {
      alert('Upload error: ' + err.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-base font-bold text-slate-900">Batch Resume Upload (PDF & DOCX)</h2>
            <p className="text-xs text-slate-500">Upload at least 10 candidate resumes in one batch.</p>
          </div>
          {uploadedResumes.length > 0 && (
            <button
              onClick={() => setUploadedResumes([])}
              className="px-3 py-1.5 bg-slate-50 hover:bg-slate-100 text-rose-600 border border-slate-200 rounded-lg text-xs font-semibold cursor-pointer"
            >
              Clear All
            </button>
          )}
        </div>

        <label className="border-2 border-dashed border-slate-300 hover:border-indigo-500 rounded-2xl p-8 flex flex-col items-center justify-center cursor-pointer bg-slate-50 hover:bg-white transition-colors">
          <UploadCloud className="w-10 h-10 text-indigo-600 mb-2" />
          <span className="text-sm font-bold text-slate-800">Select or Drag & Drop Candidate Resumes</span>
          <span className="text-xs text-slate-500 mt-1">Supports PDF (.pdf) and DOCX (.docx)</span>
          <input type="file" multiple accept=".pdf,.docx,.txt" onChange={handleFileUpload} className="hidden" />
        </label>

        {uploading && <div className="mt-4 text-xs text-indigo-600 font-medium">Extracting candidate details...</div>}
      </div>

      {uploadedResumes.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-900">Loaded Resumes ({uploadedResumes.length})</h3>
            <button
              onClick={onProceed}
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-semibold flex items-center space-x-1 shadow-xs cursor-pointer"
            >
              <span>Proceed to Matching Config</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {uploadedResumes.map((r, i) => (
              <div key={i} className="bg-white border border-slate-200 p-4 rounded-xl text-xs shadow-2xs hover:border-indigo-300 transition-all">
                <div className="flex justify-between font-bold text-slate-900 mb-1">
                  <span>{r.name}</span>
                  <span className="text-indigo-600 font-semibold">{r.experience_years} yrs</span>
                </div>
                <div className="text-[11px] text-slate-500 truncate">{r.email}</div>
                <div className="text-[11px] text-slate-500 truncate">{r.education}</div>
                <div className="mt-2 text-[10px] text-slate-400">Skills: {r.skills?.slice(0, 4).join(', ')}...</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
