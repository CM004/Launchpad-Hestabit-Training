import Input from "@/components/ui/Input";

export default function DataTable() {
  return (
      <div className="flex justify-between items-center p-3 bg-white ">

        <div className="flex items-center gap-4 text-black">
          <span>Show</span>
          <select className="border rounded px-5 py-2 text-gray-500">
            <option>5</option>
            <option>10</option>
            <option>15</option>
            <option>20</option>
          </select>
          <span>entries</span>
        </div>

        <div className="flex items-center gap-2 text-black">
          <p>Search:</p>
          <span><Input placeholder="Seach table by..." /></span>
        </div>

      </div>
  );
}