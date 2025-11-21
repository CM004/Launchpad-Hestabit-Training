export default function Badge({ children, className = "",color="" }) {
  const base = "inline-block px-2 py-1 text-sm font-semibold rounded-full";

  const colors = {
    red: "bg-red-500 text-red-700",
    green: "bg-green-500 text-green-700",
    blue: "bg-blue-500 text-blue-700",
    yellow: "bg-yellow-500 text-yellow-700",
    gray: "bg-gray-500 text-gray-700",
  };

  const badgeColor = colors[color] || colors.blue;
  
  return (
    <span className={`${base} ${className} ${badgeColor}`.trim()}>
      {children}
    </span>
  );
}