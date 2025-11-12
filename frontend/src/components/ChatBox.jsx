import { useState } from 'react';
import MessageBubble from './MessageBubble';
import { sendMessage } from '../api';

export default function ChatBox({ onNewMessage }) {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim() || loading) return;
    const userMsg = input;
    setInput('');
    onNewMessage(userMsg, true);
    setLoading(true);

    try {
      const res = await sendMessage(userMsg);
      onNewMessage(res.data.response, false);
    } catch (err) {
      onNewMessage("Sorry, I'm having trouble connecting.", false);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h2 className="text-xl font-bold text-gray-800 mb-4">AI Assistant</h2>
      <div className="h-64 overflow-y-auto mb-4 p-3 bg-gray-50 rounded-lg">
        <p className="text-sm text-gray-500 italic">Ask about shifts or report a call-off...</p>
      </div>
      <div className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="e.g., I can't take my 9 AM shift tomorrow"
          className="flex-1 px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
          disabled={loading}
        />
        <button
          onClick={handleSend}
          disabled={loading}
          className="px-6 py-3 bg-primary text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
        >
          {loading ? '...' : 'Send'}
        </button>
      </div>
    </div>
  );
}