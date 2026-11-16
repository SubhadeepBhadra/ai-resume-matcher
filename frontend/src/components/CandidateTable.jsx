import React, { useState, useMemo } from 'react';
import { Search, Download, ChevronRight, ArrowUpDown } from 'lucide-react';

export default function CandidateTable({ candidates, onSelectCandidate, searchQuery, setSearchQuery, jobTitle }) {
  const [sortField, setSortField] = useState('rank');
  const [sortAsc, setSortAsc] = useState(true);

  const getScoreBadge = (score) => {
    if (score >= 80) return 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20';
    if (score >= 65) return 'bg-blue-500/10 text-blue-400 border border-blue-500/20';
    if (score >= 50) return 'bg-amber-500/10 text-amber-400 border border-amber-500/20';
    return 'bg-rose-500/10 text-rose-400 border border-rose-500/20';
  };

  const filtered = useMemo(() => {
    let list = [...candidates];
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      list = list.filter(c =>
        c.name.toLowerCase().includes(q) ||
        c.matched_skills.some(s => s.toLowerCase().includes(q))
      );
    }
    list.sort((a, b) => {
      const valA = a[sortField];
      const valB = b[sortField];
      return sortAsc ? (valA > valB ? 1 : -1) : (valA < valB ? 1 : -1);
    });
    return list;
  }, [candidates, searchQuery, sortField, sortAsc]);

  const handleExportCSV = () => {
    if (!candidates.length) return;
    const headers = ['Rank', 'Candidate', 'Experience', 'Match %', 'Matched Skills'];
    const rows = candidates.map(c => [c.rank, `"${c.name}"`, `"${c.experience_display}"`, `${c.match_percentage}%`, `"${c.matched_skills.join(', ')}"`]);
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
    const encoded = encodeURI(csvContent);
    const link = document.createElement('a');
    link.href = encoded;
    link.download = `Candidate_Ranking_${new Date().toISOString().slice(0, 10)}.csv`;
    link.click();
  };

  return (
    <div className="space-y-4">
      <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-2xl flex flex-col sm:flex-row justify-between items-center gap-3">
        <div>
          <h2 className="text-base font-bold text-white">Candidate Ranking Dashboard</h2>
          <p className="text-xs text-slate-400">Ranked against: <span className="text-blue-400 font-semibold">{jobTitle || 'Role'}</span></p>
        </div>
        <div className="flex items-center space-x-3 w-full sm:w-auto">
          <div className="relative flex-1 sm:w-60">
            <Search className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search candidate or skill..."
              className="bg-slate-950 text-slate-200 text-xs pl-9 pr-3 py-2 rounded-xl border border-slate-800 w-full focus:outline-none focus:border-blue-500"
            />
          </div>
          <button
            onClick={handleExportCSV}
            className="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-medium border border-slate-700 flex items-center space-x-1"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export CSV</span>
          </button>
        </div>
      </div>

      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl overflow-hidden">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-950 text-slate-400 uppercase tracking-wider text-[11px] font-semibold border-b border-slate-800">
            <tr>
              <th className="py-3 px-4 w-12 cursor-pointer" onClick={() => { setSortField('rank'); setSortAsc(!sortAsc); }}>Rank</th>
              <th className="py-3 px-4 cursor-pointer" onClick={() => { setSortField('name'); setSortAsc(!sortAsc); }}>Candidate</th>
              <th className="py-3 px-4 cursor-pointer" onClick={() => { setSortField('experience_years'); setSortAsc(!sortAsc); }}>Experience</th>
              <th className="py-3 px-4 cursor-pointer" onClick={() => { setSortField('match_percentage'); setSortAsc(!sortAsc); }}>Match %</th>
              <th className="py-3 px-4">Matched Skills</th>
              <th className="py-3 px-4 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {filtered.map((c) => (
              <tr
                key={c.id}
                onClick={() => onSelectCandidate(c)}
                className="hover:bg-slate-800/40 transition-colors cursor-pointer group"
              >
                <td className="py-3.5 px-4 font-bold text-slate-400">#{c.rank}</td>
                <td className="py-3.5 px-4 font-semibold text-white group-hover:text-blue-400">{c.name}</td>
                <td className="py-3.5 px-4 text-slate-300">{c.experience_display}</td>
                <td className="py-3.5 px-4">
                  <span className={`text-xs font-bold px-2 py-0.5 rounded ${getScoreBadge(c.match_percentage)}`}>
                    {c.match_percentage}%
                  </span>
                </td>
                <td className="py-3.5 px-4">
                  <div className="flex flex-wrap gap-1 max-w-md">
                    {c.matched_skills.slice(0, 4).map((s, i) => (
                      <span key={i} className="bg-emerald-950/40 text-emerald-300 border border-emerald-800/40 px-1.5 py-0.5 rounded text-[10px]">
                        {s}
                      </span>
                    ))}
                    {c.matched_skills.length > 4 && (
                      <span className="text-slate-500 text-[10px]">+{c.matched_skills.length - 4} more</span>
                    )}
                  </div>
                </td>
                <td className="py-3.5 px-4 text-right">
                  <button className="px-2.5 py-1 bg-blue-600/20 text-blue-300 rounded text-xs inline-flex items-center space-x-1">
                    <span>Inspect</span>
                    <ChevronRight className="w-3 h-3" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
