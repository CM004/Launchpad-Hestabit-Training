import Image from "next/image";

export default function Userprofile() {
  return (
    <div className="w-full bg-white border -lg p-6 shadow-sm">
      <div className="flex flex-col md:flex-row w-full gap-6">
        <div className="w-full md:w-1/3 flex justify-center md:justify-start">
          <Image
            src="/profile.png"
            alt="Profile"
            width={200}
            height={200}
            className= "object-cover w-48 h-48 ml-25"
          />
        </div>
        <div className="flex flex-col md:flex-row w-full justify-between">
          <div className="flex-1 space-y-3 mr-6">
            <div>
              <p className="text-sm text-gray-500">Name</p>
              <p className="font-semibold text-gray-800">Chandramohan</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Job Title</p>
              <p className="font-semibold text-gray-800">Traniee Software Engineer</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Email</p>
              <a className="text-blue-600 hover:underline" href="#">
                chandramohan.hestabit@gmail.com
              </a>
            </div>
          </div>
          <div className="flex-1 space-y-3 mt-4 md:mt-0">
            <div>
              <p className="text-sm text-gray-500">LinkedIn</p>
              <a className="text-blue-600 hover:underline" href="#">
                linkedin.com
              </a>
            </div>
            <div>
              <p className="text-sm text-gray-500">Twitter</p>
              <a className="text-blue-600 hover:underline" href="#">
                www.x.com
              </a>
            </div>

            <div>
              <p className="text-sm text-gray-500">Facebook</p>
              <a className="text-blue-600 hover:underline" href="#">
                facebook.com
              </a>
            </div>
          </div>
        </div>
      </div>
      <div className="mt-6 border-t pt-4">
        <p className="text-sm font-semibold text-gray-700 mb-1">Bio</p>
        <p className="text-gray-600 text-sm leading-relaxed">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent
          aliquet odio augue, in dapibus lacus imperdiet ut. Quisque elementum
          placerat neque rhoncus tempus. Cras id suscipit diam, sit amet
          rutrum ipsum. Vestibulum rutrum elit lacinia sapien porta pulvinar.
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent
          aliquet odio augue, in dapibus lacus imperdiet ut. Quisque elementum
          placerat neque rhoncus tempus. Cras id suscipit diam, sit amet
          rutrum ipsum. Vestibulum rutrum elit lacinia sapien porta pulvinar.
        </p>
      </div>
      <button className="mt-4 text-blue-600 hover:underline text-sm">
        Edit Profile
      </button>
    </div>
  );
}