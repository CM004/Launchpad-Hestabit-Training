"use client";

export default function Modal({ isOpen, CloseModal, title, children }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-lg w-11/12 max-w-md p-6 relative">
        <button
          className="absolute top-2 right-2 text-gray-600 hover:text-gray-800"
          onClick={CloseModal}
          aria-label="Close modal"
        >
          &times;
        </button>

        {title && <h2 className="text-2xl text-black font-bold mb-4">{title}</h2>}

        <div>{children}</div>
      </div>
    </div>
  );
}
