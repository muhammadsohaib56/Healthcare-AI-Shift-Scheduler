export default function MessageBubble({ text, isUser }) {
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-3`}>
      <div
        className={`max-w-xs md:max-w-md px-4 py-3 rounded-2xl shadow-sm ${
          isUser
            ? 'bg-primary text-white'
            : 'bg-white text-gray-800 border'
        }`}
      >
        {text}
      </div>
    </div>
  );
}