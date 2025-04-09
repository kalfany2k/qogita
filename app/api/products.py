from app import models, schemas
from app.database import get_db
import codecs
import csv
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import ValidationError
from sqlalchemy.orm import Session
import xml.etree.ElementTree as ET

router = APIRouter(
    tags=['Products'],
    prefix="/products"
)

@router.post("/csv")
def post_products_from_csv(
    csv_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    db.query(models.Product).filter(models.Product.resource_identifier == "csv").delete()
    if csv_file.filename.endswith("csv"):
        csvReader = csv.DictReader(codecs.iterdecode(csv_file.file, 'utf-8'))
        for row in csvReader:
            try:
                # Validate each row, and replace GTIN & pack_size values to null, since they are not mandatory
                product_data = schemas.CSVInput(
                    product_name=row["Product Title"],
                    price=row["Variant Price"],
                    SKU=row["Variant Sku"],
                    GTIN=row["Variant Barcode"],
                    stock_quantity=row["Variant Inventory Quantity"],
                    pack_size=row["Product.custom.pack_size"]
                )

                # Create the database object
                product_model = models.Product(resource_identifier="csv", brand=None, portfolio=None, volume=None, **product_data.model_dump())

                db.add(product_model)
                db.commit()
            except ValidationError as e:
                print(f'ERROR:Encountered an error for product {row["Product Title"]} in field(s) {", ".join([",".join(error["loc"]) for error in e.errors()])}: {
                    ", ".join([error["msg"] for error in e.errors()])
                }')
                db.rollback()
                continue

@router.post("/xml")
def post_products_from_xml(
    xml_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    db.query(models.Product).filter(models.Product.resource_identifier == "xml").delete()
    if xml_file.filename.endswith("xml"):
        tree = ET.parse(xml_file.file)
        # Parse the second XML child of productFeed, items
        root = tree.getroot()[1]

        for item in root.findall("item"):
            try:
                product_data = schemas.XMLInput(
                    GTIN=item.find("articleEAN").text,
                    brand=item.find("brand").text,
                    # Beautify input
                    portfolio=item.find("portfolio").text.replace("_", " ").capitalize(),
                    product_name=item.find("articleName").text,
                    volume=item.find("volume").text,
                    price=item.find("priceWithoutVat").text,
                    stock_quantity=item.find("stockQuantity").text,
                )

                product_model = models.Product(resource_identifier="xml", SKU=None, **product_data.model_dump())

                db.add(product_model)
                db.commit()
            except ValidationError as e:
                print(f'ERROR:Encountered an error for product {item.find("articleName").text} in field(s) {", ".join([",".join(error["loc"]) for error in e.errors()])}: {
                    ", ".join([error["msg"] for error in e.errors()])
                }')
                db.rollback()
                continue

@router.get("")
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()

    return products

@router.delete("/{id}")
def remove_product(id: int, db: Session = Depends(get_db)):
        queried_product = db.query(models.Product).filter(models.Product.id == id).first()

        if not queried_product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Product with identifier {id} was not deleted, resource does not exist')

        try:
            db.delete(queried_product)
            db.commit()

            return { 
                "status_code": status.HTTP_200_OK,
                "detail": "Product successfully deleted",
                "product": queried_product 
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )