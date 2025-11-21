export default function Card({ title, content, children, icon, className=""}) {
    const base = "border rounded-lg p-4 shadow-md bg-white";
    return (
        <div className = {`${base} ${className}`.trim()}>

        <div className="flex items-center gap-3 mb-3">
        <span className="text-3xl mb-4 block">{icon}</span>
        <h3 className="text-xl font-semibold mb-2">{title}</h3>
        </div>

        <p className="text-gray-700">{content}</p>
        {children}
      </div>
    );
  }