package com.github.L_Ender.cataclysm.client.render.entity;

import com.github.L_Ender.cataclysm.client.model.CMModelLayers;
import com.github.L_Ender.cataclysm.client.model.entity.Labubu_Model;
import com.github.L_Ender.cataclysm.entity.Pet.Labubu_Entity;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.resources.ResourceLocation;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.api.distmarker.OnlyIn;

@OnlyIn(Dist.CLIENT)
public class Labubu_Renderer extends MobRenderer<Labubu_Entity, Labubu_Model> {
    private static final ResourceLocation LABUBU_TEXTURE_0 = new ResourceLocation("cataclysm:textures/entity/labubu.png");
    private static final ResourceLocation LABUBU_TEXTURE_1 = new ResourceLocation("cataclysm:textures/entity/labubu_variant1.png");
    private static final ResourceLocation LABUBU_TEXTURE_2 = new ResourceLocation("cataclysm:textures/entity/labubu_variant2.png");

    public Labubu_Renderer(EntityRendererProvider.Context context) {
        super(context, new Labubu_Model(context.bakeLayer(CMModelLayers.LABUBU_MODEL)), 0.25F);
    }

    @Override
    public void render(Labubu_Entity entity, float entityYaw, float partialTicks, PoseStack poseStack, MultiBufferSource bufferIn, int packedLightIn) {
        if (entity.isBaby()) {
            poseStack.scale(0.5F, 0.5F, 0.5F);
        }
        super.render(entity, entityYaw, partialTicks, poseStack, bufferIn, packedLightIn);
    }

    @Override
    public ResourceLocation getTextureLocation(Labubu_Entity entity) {
        switch (entity.getVariant()) {
            case 0:
            default:
                return LABUBU_TEXTURE_0;
            case 1:
                return LABUBU_TEXTURE_1;
            case 2:
                return LABUBU_TEXTURE_2;
        }
    }
}