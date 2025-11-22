export default function Input({ className = "", type = "text", placeholder = "", ...rest }) { //default props
  const base = "w-full px-3 py-2 border rounded-md focus:ring focus:ring-blue-300";
  return (
    <input
      type={type}
      placeholder={placeholder}
      className={`${base} ${className}`.trim()}
      {...rest}           //like onChange, id, aria-*, etc. 
    />
  );
}
