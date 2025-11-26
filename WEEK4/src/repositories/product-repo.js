class productRepository{
    constructor (productModel){
        this.productModel=productModel;
    }
    async createProduct(productData){
        const newProduct=new this.productModel (productData);
        return await newProduct.save();
    }
    async findAllProducts(){
        return await this.productModel.find({});
    }
    async findProductById(id){
        return await this.productModel.findById(id);
    }
    async findPaginatedProducts(page=1,limit=10){
        const skip=(page-1)*limit;
        const products=await this.productModel.find().skip(skip).limit(limit);
        const total=await this.productModel.countDocuments();
        return {
            products,
            total,
            page,
            pages:Math.ceil(total/limit)
        };
    }
    async updateProduct(id,updateData){
        return await this.productModel.findByIdAndUpdate(id,updateData,{new:true});
    }
    async deleteProduct(id){
        return await this.productModel.findByIdAndDelete(id);
    }
}