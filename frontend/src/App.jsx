import React, { useState, useEffect } from 'react';
import { Sparkles, Play } from 'lucide-react';
import JobDescriptionSection from './components/JobDescriptionSection';
import ResumeUploadSection from './components/ResumeUploadSection';
import CandidateTable from './components/CandidateTable';
import CandidateModal from './components/CandidateModal';
import WeightsConfig from './components/WeightsConfig';

export default function App() {
  const [activeTab, setActiveTab] = useState('match');
  const [jdText, setJdText] = useState('');
  const [selectedJdId, setSelectedJdId] = useState('jd-1');
  const [parsedJD, setParsedJD] = useState(null);
  const [uploadedResumes, setUploadedResumes] = useState([]);
  const [rankedCandidates, setRankedCandidates] = useState([]);
  const [isMatching, setIsMatching] = useState(false);
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [weights, setWeights] = useState({
    skills: 0.45,
    semantic: 0.35,
    experience: 0.15,
    education: 0.05
  });

  const handleLoadDemo = async (presetId = 'jd-1') => {
    setIsMatching(true);
    try {
      const res = await fetch(`/api/samples/load-preloaded?jd_id=${presetId}`);
      const data = await res.json();
      if (data.ranking) {
        setParsedJD(data.job_description);
        setJdText(data.job_description.raw_text);
        setUploadedResumes(data.ranking);
        setRankedCandidates(data.ranking);
        setActiveTab('ranking');
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsMatching(false);
    }
  };

  const handleRunMatch = async () => {
    if (!parsedJD && !jdText.trim()) return alert('Please analyze a Job Description first.');
    if (uploadedResumes.length === 0) return alert('Please upload resumes first.');

    setIsMatching(true);
    try {
      let targetJD = parsedJD;
      if (!targetJD) {
        const jdRes = await fetch('/api/jd/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: jdText })
        });
        const jdData = await jdRes.json();
        targetJD = jdData.job_description;
        setParsedJD(targetJD);
      }

      const res = await fetch('/api/match', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          jd: targetJD,
          resumes: uploadedResumes,
          weights
        })
      });
      const data = await res.json();
      if (data.ranking) {
        setRankedCandidates(data.ranking);
        setActiveTab('ranking');
      }
    } catch (err) {
      alert('Matching failed: ' + err.message);
    } finally {
      setIsMatching(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 font-sans">
      <header className="border-b border-slate-200 bg-white sticky top-0 z-40 px-6 py-3.5 shadow-xs flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center shadow-sm shadow-indigo-200 text-white">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-base font-bold text-slate-900 tracking-tight">MatchWise AI</span>
              <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200/60">
                NLP & Embeddings
              </span>
            </div>
            <p className="text-xs text-slate-500">AI-Based Resume Matching & Candidate Ranking Platform</p>
          </div>
        </div>

        <button
          onClick={() => handleLoadDemo('jd-1')}
          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-semibold text-xs shadow-xs hover:shadow-md flex items-center space-x-2 transition-all cursor-pointer"
        >
          <Play className="w-3.5 h-3.5 fill-white" />
          <span>Load 12 Sample Resumes & Demo</span>
        </button>
      </header>

      <div className="border-b border-slate-200 bg-white px-6 flex space-x-8 text-sm">
        {[
          { id: 'jd', label: '1. Job Description' },
          { id: 'resumes', label: '2. Batch Resumes' },
          { id: 'match', label: '3. Matching Engine' },
          { id: 'ranking', label: '4. Candidate Ranking' }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`py-3.5 border-b-2 font-medium cursor-pointer transition-colors ${
              activeTab === tab.id ? 'border-indigo-600 text-indigo-600 font-semibold' : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <main className="flex-1 p-6 max-w-7xl mx-auto w-full">
        {activeTab === 'jd' && (
          <JobDescriptionSection
            jdText={jdText}
            setJdText={setJdText}
            selectedJdId={selectedJdId}
            setSelectedJdId={setSelectedJdId}
            parsedJD={parsedJD}
            setParsedJD={setParsedJD}
            onProceed={() => setActiveTab('resumes')}
          />
        )}
        {activeTab === 'resumes' && (
          <ResumeUploadSection
            uploadedResumes={uploadedResumes}
            setUploadedResumes={setUploadedResumes}
            onProceed={() => setActiveTab('match')}
          />
        )}
        {activeTab === 'match' && (
          <WeightsConfig
            weights={weights}
            setWeights={setWeights}
            parsedJD={parsedJD}
            uploadedResumes={uploadedResumes}
            onRunMatch={handleRunMatch}
            isMatching={isMatching}
          />
        )}
        {activeTab === 'ranking' && (
          <CandidateTable
            candidates={rankedCandidates}
            onSelectCandidate={setSelectedCandidate}
            searchQuery={searchQuery}
            setSearchQuery={setSearchQuery}
            jobTitle={parsedJD?.title}
          />
        )}
      </main>

      {selectedCandidate && (
        <CandidateModal
          candidate={selectedCandidate}
          parsedJD={parsedJD}
          onClose={() => setSelectedCandidate(null)}
        />
      )}
    </div>
  );
}
