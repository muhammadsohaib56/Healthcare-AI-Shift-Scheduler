// frontend/src/components/ScheduleTable.jsx
import { format } from 'date-fns';

export default function ScheduleTable({ schedule }) {
  if (!schedule || schedule.length === 0) {
    return (
      <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
        <p className="text-gray-500">No shifts scheduled this week.</p>
      </div>
    );
  }

  const parseDateTime = (str) => {
    if (!str) return null;
    const [date, time] = str.split(' ');
    if (!date || !time) return null;
    
    // Fix common issues: "9:00" → "09:00", "9:0" → "09:00"
    const normalizedTime = time.length === 4 ? `0${time}` : time.padStart(5, '0');
    if (normalizedTime.length !== 5 || !normalizedTime.includes(':')) return null;

    const dateTimeStr = `${date}T${normalizedTime}:00`;
    const dateObj = new Date(dateTimeStr);
    
    return isNaN(dateObj.getTime()) ? null : dateObj;
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
      <div className="bg-gradient-to-r from-blue-600 to-indigo-700 p-5">
        <h2 className="text-xl font-bold text-white flex items-center">
          <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          This Week's Schedule
        </h2>
      </div>

      <div className="max-h-96 overflow-y-auto">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200 sticky top-0 z-10">
            <tr>
              <th className="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">Provider</th>
              <th className="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">Date</th>
              <th className="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">Time</th>
              <th className="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {schedule.map((s) => {
              const start = parseDateTime(s.shift_start);
              const end = parseDateTime(s.shift_end);

              const displayTime = start && end 
                ? `${format(start, 'h:mm a')} – ${format(end, 'h:mm a')}`
                : '—';

              const displayDate = start 
                ? `${format(start, 'EEEE')}, ${format(start, 'MMM d')}`
                : '—';

              return (
                <tr key={s.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 font-medium text-gray-900 flex items-center space-x-3">
                    <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center text-white font-bold text-sm">
                      {s.provider_name.split(' ').map(n => n[0]).join('')}
                    </div>
                    <span>{s.provider_name}</span>
                  </td>
                  <td className="px-6 py-4 text-gray-700">
                    <div>
                      <p className="font-semibold">{displayDate}</p>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-gray-700">
                    <p className="font-mono font-semibold">{displayTime}</p>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex items-center px-4 py-2 rounded-full text-xs font-bold uppercase tracking-wider ${
                      s.status === 'called_off'
                        ? 'bg-red-100 text-red-700 border border-red-300'
                        : 'bg-green-100 text-green-700 border border-green-300'
                    }`}>
                      {s.status === 'called_off' ? 'Called Off' : 'Active'}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}