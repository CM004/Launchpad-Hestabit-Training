class productRepository{
    constructor (productModel){
        this.productModel=productModel;
    }
    async createProduct(productData){
        const newProduct=new this.productModel (productData);
        return await newProduct.save();
    }
    async findAllProducts(){
        return await this.productModel.find({isDeleted: false});
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

    //DAY3

    async findProductsWithFilters(filter,options={}){
        const {sort, skip, limit}=options;
        let query =this.productModel.find(filter);
        if(sort){
            query=query.sort(sort);
        }
        if(skip !==undefined){
            query=query.skip(skip);
        }
        if(limit){
            query=query.limit(limit);
        }

        return await query;
    };


    async countProductsWithFilters(filter){
        return await this.productModel.countDocuments(filter);
    }

    async softDeleteProduct(id){
        return await this.productModel.findByIdAndUpdate(
            id,
            {isDeleted:true, deletedAt: new Date()},
            {new:true}
        );
    }

    async restoreSoftDeletedProduct(id){
        return await this.productModel.findByIdAndUpdate(
            id,
            {isDeleted:false, deletedAt:null},
            {new:true}
        );
    }

}

module.exports=productRepository;