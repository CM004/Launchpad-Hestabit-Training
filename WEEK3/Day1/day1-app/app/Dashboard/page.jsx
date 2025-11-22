import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import Modal from "@/components/ui/Modal";
import Input from "@/components/ui/Input";
import DataTable from "@/components/ui/DataTable";

import AreaChart from "@/components/charts/AreaChart";
import BarChart from "@/components/charts/BarChart";
import {FaChartArea, FaChartBar, FaTable } from "react-icons/fa";

export default function Home() {
    return (
    <div className=" bg-gray-100 p-3">
        <h1 className="text-5xl text-black font-bold">Dashboard

        </h1>
            <div className="bg-white shadow rounded p-3 text-gray-600 mt-3">
                Dashboard   
            </div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-6">
                <Card title="Primary Card" className="bg-blue-500">
                    <hr className="border-t border-blue-700"/>
                    <div className="mt-2">
                        <Button size="sm" type="primary" className="w-full h-9 text-left">
                            View Details
                        </Button>
                    </div>
                </Card>

                <Card title="Warning Card" className="bg-yellow-500">
                    <hr className="border-t border-yellow-600"/>
                    <div className="mt-2">
                        <Button size="sm" type="secondary" className="w-full h-9 text-left">
                            View Details
                        </Button>
                    </div>
                </Card>

                <Card title="Success Card" className="bg-green-500">
                    <hr className="border-t border-green-600"/>
                    <div className="mt-2">
                        <Button size="sm" type="basic" className="w-full h-9 text-left">
                            View Details
                        </Button>
                    </div>
                </Card>

                <Card title="Danger Card" className="bg-red-500">
                    <hr className="border-t border-red-700"/>
                    <div className="mt-2">
                        <Button size="sm" type="delete" className="w-full h-9 text-left">
                            View Details
                        </Button>
                    </div>
                </Card>

        </div> 

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6 mt-6">

              <Card title="Area Chart Example" icon={<FaChartArea />} className="bg-purple-600" >
                <div className="h-64 flex justify-center bg-white">
                  <AreaChart/>
                </div>
              </Card>

              <Card title="Bar Chart Example" icon={<FaChartBar />} className="bg-amber-700">
                <div className="h-64 flex justify-center bg-white">
                  <BarChart/>
                </div>
              </Card>
            </div>
        <div>
        <Card title="Data Table " icon={<FaTable />} className="bg-gray-300">
        <div className="-mx-4 -mb-4 -my-4">
        
        <DataTable />

        </div>
        </Card>
        </div>

    </div>  
    
  );
}